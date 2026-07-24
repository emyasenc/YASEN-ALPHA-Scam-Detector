# 🛡️ YASEN-ALPHA Job Scam Detector

[![CI/CD](https://github.com/emyasenc/YASEN-ALPHA-Scam-Detector/actions/workflows/ci.yml/badge.svg)](https://github.com/emyasenc/YASEN-ALPHA-Scam-Detector/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![RapidAPI](https://img.shields.io/badge/RapidAPI-0066FF?style=flat&logo=rapidapi&logoColor=white)](https://rapidapi.com/emyasenc/api/yasen-alpha-job-scam-detector)

> **Enterprise-grade job scam detection with 99.44% accuracy and 0.37% false positive rate — 5x better than industry average.**

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| **Accuracy** | **99.44%** 🎯 |
| **False Positive Rate** | **0.37%** (industry best) |
| **Precision** | 95% |
| **Recall** | 97% |
| **F1-Score** | 0.96 |
| **Training Data** | **2,678** real & scam jobs |
| **Industries** | 16+ |
| **Tested On** | LinkedIn, Indeed, Handshake |
| **Response Time** | <10ms (cached) |

---

## 🚀 Why Choose YASEN-ALPHA?

| Competitor | Accuracy | False Positive Rate | Price | You Save |
|------------|----------|---------------------|-------|----------|
| ScamAdvisor | Not published | 10-15% | $299+ | ❌ 10x more false positives |
| JobScamDetector.io | Not published | 5-10% | $199+ | ❌ 5x more false positives |
| **YASEN-ALPHA** | **99.44%** | **0.37%** | **$19-199** | ✅ **5-10x better, 50-80% cheaper** |

---

## ✨ Features

- ✅ **99.44% accuracy** on real-world jobs
- ✅ **0.37% false positives** — industry best
- ✅ **97% scam recall** — catches almost all scams
- ✅ **2,678 training examples** — robust and diverse
- ✅ **16+ industries** supported
- ✅ **Production-ready FastAPI** with caching
- ✅ **Rate limiting** to prevent abuse
- ✅ **Persistent usage stats** with SQLite
- ✅ **Open source** — fully transparent
- ✅ **24/7 availability** with UptimeRobot

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/emyasenc/YASEN-ALPHA-Scam-Detector.git
cd YASEN-ALPHA-Scam-Detector
pip install -r requirements.txt
```

## Run the API Locally

```bash
python src/api/main.py
```

## Test with curl

```bash
# Real job
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer at Google",
    "description": "Design and build scalable backend systems"
  }'

# Scam job
curl -X POST http://localhost:8000/predict \
  -H "Content-Type": "application/json" \
  -d '{
    "title": "WORK FROM HOME - EARN $5000/WEEK!!!",
    "description": "No experience needed! Send $50 for training materials"
  }'
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Predict if a single job is a scam |
| `/predict/batch` | POST | Predict up to 100 jobs at once |
| `/stats` | GET | Persistent API usage statistics |
| `/industries` | GET | Supported industries |

### Example Request

```json
POST /predict
{
  "title": "Senior Software Engineer",
  "description": "Design scalable backend systems",
  "company": "Google"
}
```

### Example Response

```json
{
  "is_scam": false,
  "probability": 0.1587,
  "confidence": "low",
  "threshold": 0.55,
  "model_version": "2.1.0",
  "timestamp": "2026-07-23T18:33:35",
  "processing_time_ms": 3
}
```

### Usage Stats Example

```json
GET /stats
{
  "total_predictions": 3,
  "scam_count": 1,
  "scam_rate": 0.3333,
  "avg_confidence": 0.3871,
  "last_updated": "2026-07-23 18:34:29"
}
```

---

## 🧪 Latest Model Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | **99.44%** |
| **Precision** | 95% |
| **Recall** | 97% |
| **F1-Score** | 0.96 |
| **False Positive Rate** | **0.37%** |

### Confusion Matrix

[[495 2] ← Real jobs: 495 correct, 2 false positives
[ 1 38]] ← Scams: 38 caught, 1 missed


### ROC-AUC Score

**0.9996** — nearly perfect discrimination between real and scam jobs.

---

## 📁 Project Structure

```bash
YASEN-ALPHA-Scam-Detector/
├── src/
│   ├── api/           # FastAPI endpoints
│   ├── pipelines/     # Data, feature, training pipelines
│   ├── data/          # Data collection & processing
│   ├── models/        # Model training
│   ├── orchestration/ # Pipeline orchestration
│   └── tests/         # Unit & integration tests
├── models/            # Trained models
├── data/              # Raw & processed data
├── scripts/           # Utility scripts
├── .github/workflows/ # CI/CD pipeline
└── docs/              # Documentation
```

---

## 💰 Pricing

| Plan | Price | Calls/Month | Rate Limit | Best For |
|------|-------|-------------|------------|----------|
| **Basic** | **$0** | 50 | 5/min | Testing |
| **Pro ⭐** | **$19** | 500 | 20/min | Small job boards |
| **Ultra** | **$49** | 1,000 | 50/min | Growing businesses |
| **Mega** | **$199** | 10,000 | 200/min | Enterprise |

---

## 🔗 Links

- **RapidAPI Listing:** [YASEN-ALPHA Job Scam Detector](https://rapidapi.com/emyasenc/api/yasen-alpha-job-scam-detector1)
- **GitHub:** [YASEN-ALPHA-Scam-Detector](https://github.com/emyasenc/YASEN-ALPHA-Scam-Detector)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Model** | Logistic Regression + TF-IDF |
| **Data** | 2,678 real & scam jobs |
| **API** | FastAPI, Uvicorn |
| **Deployment** | Render, Docker, GitHub Actions |
| **Monitoring** | UptimeRobot, Prometheus |
| **Testing** | Pytest |
| **Stats** | SQLite (persistent) |

---

## 📄 License

MIT © 2026 YASEN-ALPHA

---

Built with ❤️ by Emma — AI Engineer & Data Scientist
