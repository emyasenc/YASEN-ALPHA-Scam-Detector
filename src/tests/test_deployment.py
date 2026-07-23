#!/usr/bin/env python3
"""
Test all API endpoints after deployment
Run this locally to verify everything works
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "https://yasen-alpha-scam-detector.onrender.com"

print("="*70)
print("🚀 TESTING DEPLOYED API")
print("="*70)
print(f"Base URL: {BASE_URL}")
print(f"Time: {datetime.now().isoformat()}")
print("="*70)

# ============================================
# 1. Health Check
# ============================================
print("\n📊 1. Testing Health Check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)[:500]}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# ============================================
# 2. Root Endpoint
# ============================================
print("\n📊 2. Testing Root Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# ============================================
# 3. Single Prediction - Real Job
# ============================================
print("\n📊 3. Testing Single Prediction (Real Job)...")
start = time.time()
try:
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"title": "Software Engineer at Google", "description": "Build scalable backend systems with Java and Python"},
        timeout=10
    )
    latency = (time.time() - start) * 1000
    print(f"   Status: {response.status_code}")
    print(f"   Latency: {latency:.0f}ms")
    data = response.json()
    print(f"   Is Scam: {data.get('is_scam')}")
    print(f"   Probability: {data.get('probability')}")
    print(f"   Confidence: {data.get('confidence')}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# ============================================
# 4. Single Prediction - Scam Job
# ============================================
print("\n📊 4. Testing Single Prediction (Scam Job)...")
start = time.time()
try:
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"title": "WORK FROM HOME - EARN $5000/WEEK!!!", "description": "No experience needed! Send $50 for training materials!"},
        timeout=10
    )
    latency = (time.time() - start) * 1000
    print(f"   Status: {response.status_code}")
    print(f"   Latency: {latency:.0f}ms")
    data = response.json()
    print(f"   Is Scam: {data.get('is_scam')}")
    print(f"   Probability: {data.get('probability')}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# ============================================
# 5. Batch Prediction
# ============================================
print("\n📊 5. Testing Batch Prediction...")
start = time.time()
try:
    response = requests.post(
        f"{BASE_URL}/predict/batch",
        json={
            "jobs": [
                {"title": "Software Engineer at Google", "description": "Build scalable systems"},
                {"title": "WORK FROM HOME - EARN $5000/WEEK!!!", "description": "Send $50 for training"},
                {"title": "Registered Nurse at Mayo Clinic", "description": "Provide patient care"}
            ]
        },
        timeout=10
    )
    latency = (time.time() - start) * 1000
    print(f"   Status: {response.status_code}")
    print(f"   Latency: {latency:.0f}ms")
    data = response.json()
    print(f"   Total: {data.get('total')}")
    print(f"   Scams Found: {data.get('scams_found')}")
    for result in data.get('results', []):
        print(f"     - {result['title'][:40]}: {'SCAM' if result['is_scam'] else 'REAL'} ({result['probability']})")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# ============================================
# 6. Stats Endpoint
# ============================================
print("\n📊 6. Testing Stats Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/stats", timeout=10)
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Total Predictions: {data.get('total_predictions')}")
    print(f"   Scam Rate: {data.get('scam_rate')}")
    print(f"   Model Accuracy: {data.get('model_accuracy')}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# ============================================
# 7. Industries Endpoint
# ============================================
print("\n📊 7. Testing Industries Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/industries", timeout=10)
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Total Industries: {data.get('total')}")
    print(f"   Industries: {data.get('industries')[:5]}... (showing first 5)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# ============================================
# 8. Rate Limit Test
# ============================================
print("\n📊 8. Testing Rate Limiting...")
for i in range(1, 8):
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"title": f"Test {i}", "description": "Testing rate limit"},
            timeout=10
        )
        if response.status_code == 429:
            print(f"   Request {i}: ⚠️ Rate limit hit! (429)")
            break
        else:
            print(f"   Request {i}: ✅ OK ({response.status_code})")
    except Exception as e:
        print(f"   Request {i}: ❌ Failed")
    time.sleep(0.1)

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)
print("\n✅ If all tests passed, your API is ready for RapidAPI!")
print("\n📝 Performance Expectations:")
print("   - Single prediction: 50-200ms")
print("   - Batch prediction (10 jobs): 200-500ms")
print("   - Health check: <50ms")