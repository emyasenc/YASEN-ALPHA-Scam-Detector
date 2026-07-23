"""
Job Scam Detector API - ENTERPRISE-GRADE
Production-ready with rate limiting, monitoring, and authentication
"""

import pickle
import re
import time
import threading
import sqlite3
import random
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Depends, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
import logging
import requests
import uvicorn
import os
import secrets

# ============================================================================
# CONFIGURATION
# ============================================================================

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load model at startup
MODEL_PATH = Path("models/production_model.pkl")
VECTORIZER_PATH = Path("models/vectorizer.pkl")
THRESHOLD_PATH = Path("models/threshold.txt")
MODEL_VERSION = "2.0.0"
MODEL_ACCURACY = 0.968

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    with open(THRESHOLD_PATH, 'r') as f:
        THRESHOLD = float(f.read().strip())
    logger.info(f"✅ Model loaded: {type(model).__name__}")
    logger.info(f"✅ Threshold: {THRESHOLD}")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    raise

SUPPORTED_INDUSTRIES = [
    "Technology", "Healthcare", "Retail", "Education", "Finance",
    "Manufacturing", "Legal", "Sales", "Food Service", "Transportation",
    "Administrative", "Marketing", "Construction", "Design", "Customer Service",
    "Remote"
]

# ============================================================================
# PROMETHEUS METRICS (optional - will work without if not installed)
# ============================================================================

try:
    from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
    
    predictions_total = Counter('predictions_total', 'Total predictions', ['result'])
    prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')
    api_requests = Counter('api_requests_total', 'Total API requests', ['endpoint', 'method'])
    error_counter = Counter('api_errors_total', 'Total API errors', ['endpoint', 'error_type'])
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("⚠️ Prometheus not installed. Metrics disabled.")

# ============================================================================
# RATE LIMITING (simpler version without slowapi to avoid issues)
# ============================================================================

class SimpleRateLimiter:
    """Simple in-memory rate limiter"""
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check if rate limit is exceeded"""
        now = time.time()
        with self.lock:
            # Clean old requests
            self.requests[key] = [t for t in self.requests[key] if now - t < window]
            
            # Check limit
            if len(self.requests[key]) >= limit:
                return False
            
            # Add current request
            self.requests[key].append(now)
            return True

rate_limiter = SimpleRateLimiter()

# ============================================================================
# API KEY AUTHENTICATION
# ============================================================================

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_keys():
    """Load API keys from environment variables"""
    keys = {}
    
    # Free tier
    free_key = os.getenv("FREE_API_KEY")
    if free_key:
        keys[free_key] = {
            "tier": "free", 
            "calls_per_month": 100, 
            "rate_limit": 5
        }
    
    # Pro tier
    pro_key = os.getenv("PRO_API_KEY")
    if pro_key:
        keys[pro_key] = {
            "tier": "pro", 
            "calls_per_month": 1000, 
            "rate_limit": 50
        }
    
    # Business tier
    business_key = os.getenv("BUSINESS_API_KEY")
    if business_key:
        keys[business_key] = {
            "tier": "business", 
            "calls_per_month": 10000, 
            "rate_limit": 200
        }
    
    # If no keys found, provide a default free tier (for development)
    if not keys:
        print("⚠️ No API keys found in environment. Using development mode.")
        keys["dev_key_123"] = {"tier": "free", "calls_per_month": 1000, "rate_limit": 100}
    
    return keys

# Load API keys at startup
API_KEYS = get_api_keys()

# ============================================================================
# API KEY VERIFICATION - THIS WAS MISSING!
# ============================================================================

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Verify API key and return tier information.
    If no key is provided, treat as free tier (for development).
    """
    if not api_key:
        return {"tier": "free", "api_key": None, "rate_limit": 5}
    
    if api_key in API_KEYS:
        return {
            "tier": API_KEYS[api_key]["tier"],
            "api_key": api_key,
            "rate_limit": API_KEYS[api_key]["rate_limit"]
        }
    
    # Invalid API key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key"
    )

# ============================================================================
# CACHE SYSTEM
# ============================================================================

class Cache:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl
        self.stats = {"hits": 0, "misses": 0}
        self.lock = threading.Lock()
        self._start_cleanup()
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                value, expiry = self.cache[key]
                if expiry > time.time():
                    self.stats["hits"] += 1
                    return value
                else:
                    del self.cache[key]
            self.stats["misses"] += 1
            return None
    
    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.ttl
        with self.lock:
            self.cache[key] = (value, time.time() + ttl)
    
    def get_stats(self):
        with self.lock:
            total = self.stats["hits"] + self.stats["misses"]
            hit_rate = f"{self.stats['hits']/total*100:.1f}%" if total > 0 else "0%"
            return {
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "hit_rate": hit_rate,
                "cache_size": len(self.cache)
            }
    
    def _start_cleanup(self):
        def cleanup():
            while True:
                time.sleep(60)
                with self.lock:
                    now = time.time()
                    to_delete = [k for k, (_, exp) in self.cache.items() if exp <= now]
                    for k in to_delete:
                        del self.cache[k]
        thread = threading.Thread(target=cleanup, daemon=True)
        thread.start()

cache = Cache(ttl=300)

# ============================================================================
# PERSISTENT STATS WITH SQLITE
# ============================================================================

class StatsDB:
    def __init__(self, db_path="stats.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with a stats table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_predictions INTEGER DEFAULT 0,
                scam_count INTEGER DEFAULT 0,
                confidence_sum REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Insert initial row if empty
        cursor.execute("SELECT COUNT(*) FROM stats")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO stats (total_predictions, scam_count, confidence_sum)
                VALUES (0, 0, 0.0)
            """)
        conn.commit()
        conn.close()

    def update(self, is_scam, probability):
        """Update stats after a prediction."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stats
            SET total_predictions = total_predictions + 1,
                scam_count = scam_count + ?,
                confidence_sum = confidence_sum + ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (1 if is_scam else 0, probability))
        conn.commit()
        conn.close()

    def get_stats(self):
        """Get current stats from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT total_predictions, scam_count, confidence_sum, last_updated
            FROM stats WHERE id = 1
        """)
        row = cursor.fetchone()
        conn.close()

        if row:
            total, scam_count, confidence_sum, last_updated = row
            scam_rate = scam_count / total if total > 0 else 0
            avg_confidence = confidence_sum / total if total > 0 else 0
            return {
                "total_predictions": total,
                "scam_count": scam_count,
                "scam_rate": round(scam_rate, 4),
                "avg_confidence": round(avg_confidence, 4),
                "last_updated": last_updated
            }
        return None

# Initialize stats database
stats_db = StatsDB("stats.db")

# ============================================================================
# CREATE FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Job Scam Detector API",
    description="Detect job scams with 96.8% accuracy. 0% false positives on LinkedIn real jobs.",
    version=MODEL_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ============================================================================
# TEXT CLEANING
# ============================================================================

def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', ' URL ', text)
    text = re.sub(r'\S+@\S+', ' EMAIL ', text)
    text = re.sub(r'\d+', ' NUMBER ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

# ✅ UPDATED: Added reasonable max_length constraints for security and performance
class JobPost(BaseModel):
    title: str = Field(
        ..., 
        description="Job title", 
        example="Senior Software Engineer",
        min_length=1,
        max_length=200  # ✅ Added: job titles are rarely longer than 200 chars
    )
    description: str = Field(
        ..., 
        description="Job description", 
        example="We are looking for...",
        min_length=1,
        max_length=5000  # ✅ Added: reasonable limit for job descriptions
    )
    company: Optional[str] = Field(
        default="", 
        description="Company name", 
        example="Google",
        max_length=100  # ✅ Added: company names are typically short
    )
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('description')
    def description_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

class BatchJobPost(BaseModel):
    jobs: List[JobPost] = Field(..., description="List of jobs to predict", max_items=100)

class PredictionResponse(BaseModel):
    is_scam: bool
    probability: float
    confidence: str
    threshold: float
    model_version: str
    timestamp: str
    processing_time_ms: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_type: str
    threshold: float
    model_accuracy: float
    version: str
    timestamp: str

# ============================================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Rate limiting check (simple)
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.check_rate_limit(client_ip, 60, 60):  # 60 requests per minute
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "code": 429, "message": "Too many requests"}
        )
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    if process_time > 1.0:
        logger.warning(f"Slow request: {request.method} {request.url.path} took {process_time:.2f}s")
    
    response.headers["X-Process-Time"] = str(process_time)
    
    if PROMETHEUS_AVAILABLE:
        api_requests.labels(endpoint=request.url.path, method=request.method).inc()
    
    return response

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    logger.info("="*60)
    logger.info("🚀 Job Scam Detector API Starting...")
    logger.info(f"Version: {MODEL_VERSION}")
    logger.info(f"Model: {type(model).__name__}")
    logger.info(f"Threshold: {THRESHOLD}")
    logger.info(f"Accuracy: {MODEL_ACCURACY*100:.1f}%")
    logger.info("="*60)
    
    # Warm up cache
    test_job = JobPost(title="Software Engineer", description="Build software")
    text = clean_text(test_job.title) + " " + clean_text(test_job.description)
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0, 1]
    cache.set("test_prediction", {"is_scam": prob >= THRESHOLD, "probability": float(prob)})
    logger.info("✅ Cache warmed up")

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", response_model=HealthResponse, tags=["Root"])
async def root():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_type": type(model).__name__,
        "threshold": THRESHOLD,
        "model_accuracy": MODEL_ACCURACY,
        "version": MODEL_VERSION,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_type": type(model).__name__,
        "threshold": THRESHOLD,
        "model_accuracy": MODEL_ACCURACY,
        "version": MODEL_VERSION,
        "cache_stats": cache.get_stats(),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(
    job: JobPost,
    request: Request,
    api_key_info: dict = Depends(verify_api_key)
):
    start_time = time.time()
    
    # Check rate limit by API key
    key_id = api_key_info.get("api_key", "free")
    rate_limit = api_key_info.get("rate_limit", 5)
    if not rate_limiter.check_rate_limit(key_id, rate_limit, 60):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Check cache
    cache_key = hashlib.md5(f"{job.title}{job.description}".encode()).hexdigest()
    cached = cache.get(cache_key)
    if cached:
        processing_time = int((time.time() - start_time) * 1000)
        cached["processing_time_ms"] = processing_time
        return cached
    
    # Predict
    text = clean_text(job.title) + " " + clean_text(job.description)
    X = vectorizer.transform([text])
    prob = float(model.predict_proba(X)[0, 1])
    is_scam = prob >= THRESHOLD
    
    # Confidence level
    if prob > 0.7:
        confidence = "high"
    elif prob > 0.3:
        confidence = "medium"
    else:
        confidence = "low"
    
    # Update stats using SQLite
    stats_db.update(is_scam, prob)
    
    if PROMETHEUS_AVAILABLE:
        predictions_total.labels(result="scam" if is_scam else "real").inc()
    
    processing_time = int((time.time() - start_time) * 1000)
    
    response = {
        "is_scam": is_scam,
        "probability": round(prob, 4),
        "confidence": confidence,
        "threshold": THRESHOLD,
        "model_version": MODEL_VERSION,
        "timestamp": datetime.now().isoformat(),
        "processing_time_ms": processing_time
    }
    
    cache.set(cache_key, response)
    logger.info(f"Prediction: {job.title[:50]} -> {'SCAM' if is_scam else 'REAL'} ({prob:.3f}) in {processing_time}ms")
    
    return response

@app.post("/predict/batch", tags=["Prediction"])
async def predict_batch(
    batch: BatchJobPost,
    request: Request,
    api_key_info: dict = Depends(verify_api_key)
):
    if len(batch.jobs) > 100:
        raise HTTPException(status_code=400, detail="Max 100 jobs per batch")
    
    results = []
    scams_found = 0
    
    for job in batch.jobs:
        text = clean_text(job.title) + " " + clean_text(job.description)
        X = vectorizer.transform([text])
        prob = float(model.predict_proba(X)[0, 1])
        is_scam = prob >= THRESHOLD
        
        if is_scam:
            scams_found += 1
        
        results.append({
            "title": job.title,
            "company": job.company or "",
            "is_scam": is_scam,
            "probability": round(prob, 4),
            "confidence": "high" if prob > 0.7 else "medium" if prob > 0.3 else "low"
        })
        
        # Update stats using SQLite for each job
        stats_db.update(is_scam, prob)
    
    return {
        "results": results,
        "total": len(batch.jobs),
        "scams_found": scams_found,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats", tags=["Info"])
async def get_stats():
    stats = stats_db.get_stats()
    if stats:
        return stats
    return {"error": "No stats available"}

@app.get("/industries", tags=["Info"])
async def get_industries():
    return {
        "industries": SUPPORTED_INDUSTRIES,
        "total": len(SUPPORTED_INDUSTRIES),
        "message": "Model tested on real jobs across these industries",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    if PROMETHEUS_AVAILABLE:
        return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    return {"error": "Metrics not enabled", "install": "pip install prometheus-client"}

@app.get("/cache-stats", tags=["Admin"])
async def get_cache_stats(api_key_info: dict = Depends(verify_api_key)):
    if api_key_info.get("tier") not in ["business", "enterprise"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return cache.get_stats()

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "code": 404, "docs": "/docs", "timestamp": datetime.now().isoformat()}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    if PROMETHEUS_AVAILABLE:
        error_counter.labels(endpoint=request.url.path, error_type="500").inc()
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "code": 500, "timestamp": datetime.now().isoformat()}
    )

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1 
    )