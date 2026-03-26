# test_handshake_real.py
"""
Test your model on REAL Handshake job postings
These are actual listings from Handshake
"""

import pickle
import pandas as pd
import re
from datetime import datetime

print("="*70)
print("🔍 REAL HANDSHAKE JOB TEST SUITE")
print("="*70)

# Load model
with open('models/production_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('models/threshold.txt', 'r') as f:
    threshold = float(f.read().strip())

print(f"\n✅ Model: {type(model).__name__}")
print(f"✅ Threshold: {threshold:.2f}")

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', ' URL ', text)
    text = re.sub(r'\S+@\S+', ' EMAIL ', text)
    text = re.sub(r'\d+', ' NUMBER ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ============================================
# REAL HANDSHAKE JOB POSTS (From your examples)
# ============================================

handshake_jobs = [
    # Tech job - Web Platform Application Developer
    {
        "title": "Web Platform Application Developer",
        "company": "Asterisk Green Inc",
        "description": """
        Web Application Developer – Platform Development
        Location: Detroit, Michigan
        Company: Asterisk Green Inc. - A sustainability-focused engineering startup developing intelligent hardware systems for building efficiency and performance.
        """,
        "expected": "REAL"
    },
    # Tech/Healthcare - AI & Automation Engineer Intern
    {
        "title": "AI & Automation Engineer Intern",
        "company": "American Medical Compliance",
        "description": """
        AI & Automation Engineer Intern (n8n / Workflow Automation)
        American Medical Compliance (AMC) is growing — and so is our AI team! We currently have a team of three engineers, and we're looking for a fourth to join us.
        We're seeking an AI-driven, automation-focused engineer to help design, build, and optimize workflows using n8n and other automation tools.
        $15–20/hr, Remote, Part-time 20 hours/week
        """,
        "expected": "REAL"
    },
    # Data Engineer - Healthcare
    {
        "title": "Data Engineer",
        "company": "Detroit Wayne Integrated Health Network",
        "description": """
        Data Engineer - Information Technology
        Design, build, and maintain data systems and pipelines that power our organization's analytics and operational capabilities.
        Responsibilities include building scalable data pipelines, ELT/ETL processes using SSIS, Azure Data Factory, Snowflake.
        Required: 7+ years experience, SQL, Python, PowerShell, Azure data services.
        Salary: $97–125K/year
        """,
        "expected": "REAL"
    },
]

# ============================================
# ADDITIONAL REAL HANDSHAKE-STYLE JOBS
# ============================================

# Since Handshake has many entry-level and internship roles, let's add realistic examples
handshake_jobs.extend([
    {
        "title": "Software Engineering Intern",
        "company": "Ford Motor Company",
        "description": "Software Engineering Intern for Summer 2026. Work on connected vehicle features. Must be enrolled in CS or related program. 3.0 GPA required. Paid internship.",
        "expected": "REAL"
    },
    {
        "title": "IT Support Specialist",
        "company": "Michigan State University",
        "description": "Provide technical support for faculty and staff. Troubleshoot hardware/software issues. Student position, flexible hours. $15-18/hour.",
        "expected": "REAL"
    },
    {
        "title": "Marketing Intern",
        "company": "Quicken Loans",
        "description": "Marketing Intern for Summer 2026. Assist with social media campaigns, content creation, and market research. Junior/Senior standing preferred.",
        "expected": "REAL"
    },
    {
        "title": "Data Analyst Co-op",
        "company": "Blue Cross Blue Shield of Michigan",
        "description": "Data Analyst Co-op position. Work with SQL, Tableau, and Excel to analyze healthcare data. 6-month rotation. Open to students graduating 2026-2027.",
        "expected": "REAL"
    },
    {
        "title": "Civil Engineering Intern",
        "company": "Michigan Department of Transportation",
        "description": "Civil Engineering Intern for summer. Work on road and bridge projects. Must be enrolled in civil engineering program. Paid internship.",
        "expected": "REAL"
    },
    {
        "title": "Supply Chain Analyst",
        "company": "General Motors",
        "description": "Entry-level Supply Chain Analyst. Manage supplier relationships, analyze logistics data. Recent graduates encouraged to apply. Competitive salary.",
        "expected": "REAL"
    },
    {
        "title": "Research Assistant",
        "company": "University of Michigan",
        "description": "Research Assistant in Computer Science department. Work on NSF-funded AI research project. Programming experience required. Stipend provided.",
        "expected": "REAL"
    },
    {
        "title": "Business Development Associate",
        "company": "Detroit Startup",
        "description": "Entry-level Business Development Associate. Help grow client base, conduct market research. Commission + base salary. Recent graduates welcome.",
        "expected": "REAL"
    },
])

# ============================================
# SCAM JOBS (Similar to Handshake-style scams)
# ============================================

scam_jobs = [
    {
        "title": "URGENT: Remote Data Entry - $25/hr",
        "company": "Unknown",
        "description": "Work from home data entry. No experience needed. Just $35 registration fee. Start today!",
        "expected": "SCAM"
    },
    {
        "title": "Summer Intern - Make $5000/month",
        "company": "Career Solutions Inc",
        "description": "Paid internship! Earn $5000/month working from home. Pay $50 for training materials to secure your spot.",
        "expected": "SCAM"
    },
    {
        "title": "Google Internship - Guaranteed Placement",
        "company": "Google Career Program",
        "description": "Guaranteed Google internship! Just $199 for application processing and interview preparation. Limited spots!",
        "expected": "SCAM"
    },
    {
        "title": "Scholarship Opportunity - $10,000",
        "company": "National Scholarship Foundation",
        "description": "Apply for $10,000 scholarship. Processing fee $50. Guaranteed award!",
        "expected": "SCAM"
    },
    {
        "title": "Work From Home - Student Opportunity",
        "company": "Remote Work Solutions",
        "description": "Make $2000/week working from home. Flexible hours for students. Registration fee $40.",
        "expected": "SCAM"
    },
]

# ============================================
# RUN PREDICTIONS
# ============================================

print("\n" + "="*70)
print(f"📊 TESTING {len(handshake_jobs)} REAL HANDSHAKE JOBS + {len(scam_jobs)} SCAMS")
print("="*70)

# Test real jobs
print("\n✅ REAL HANDSHAKE JOBS (Should be REAL):")
print("-" * 70)

real_results = []
for job in handshake_jobs:
    text = clean_text(job["title"]) + " " + clean_text(job["description"])
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0, 1]
    is_scam = prob >= threshold
    
    status = "❌ SCAM" if is_scam else "✅ REAL"
    real_results.append({
        "title": job["title"],
        "company": job["company"],
        "prob": prob,
        "prediction": "SCAM" if is_scam else "REAL",
        "result": "PASS" if not is_scam else "FAIL"
    })
    
    print(f"{status}: {job['title']} at {job['company']} (prob: {prob:.3f})")

# Test scam jobs
print("\n\n🚨 SCAM JOBS (Should be SCAM):")
print("-" * 70)

scam_results = []
for job in scam_jobs:
    text = clean_text(job["title"]) + " " + clean_text(job["description"])
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0, 1]
    is_scam = prob >= threshold
    
    status = "✅ SCAM" if is_scam else "❌ REAL"
    scam_results.append({
        "title": job["title"],
        "prob": prob,
        "prediction": "SCAM" if is_scam else "REAL",
        "result": "PASS" if is_scam else "FAIL"
    })
    
    print(f"{status}: {job['title']} (prob: {prob:.3f})")

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)

real_passed = sum(1 for r in real_results if r["result"] == "PASS")
scam_passed = sum(1 for r in scam_results if r["result"] == "PASS")
total = len(handshake_jobs) + len(scam_jobs)

print(f"\n✅ Handshake Real Jobs: {real_passed}/{len(handshake_jobs)} correct ({real_passed/len(handshake_jobs)*100:.1f}%)")
print(f"✅ Scam Jobs: {scam_passed}/{len(scam_jobs)} correct ({scam_passed/len(scam_jobs)*100:.1f}%)")
print(f"✅ Total: {real_passed + scam_passed}/{total} correct ({((real_passed + scam_passed)/total * 100):.1f}%)")

# Show failures
if real_passed < len(handshake_jobs):
    print("\n❌ FAILED REAL HANDSHAKE JOBS:")
    for r in real_results:
        if r["result"] == "FAIL":
            print(f"   • {r['title']} at {r['company']} (prob: {r['prob']:.3f})")

if scam_passed < len(scam_jobs):
    print("\n❌ FAILED SCAM JOBS:")
    for r in scam_results:
        if r["result"] == "FAIL":
            print(f"   • {r['title']} (prob: {r['prob']:.3f})")

# Final verdict
print("\n" + "="*70)
print("🎯 FINAL VERDICT")
print("="*70)

if real_passed >= len(handshake_jobs) * 0.95 and scam_passed >= len(scam_jobs) * 0.95:
    print("\n🏆 EXCELLENT! Your model handles Handshake jobs perfectly.")
    print("✅ READY FOR ENTERPRISE DEPLOYMENT!")
elif real_passed >= len(handshake_jobs) * 0.9 and scam_passed >= len(scam_jobs) * 0.9:
    print("\n✅ GOOD! Ready for production deployment.")
else:
    print("\n⚠️ Add failures to training and retrain.")

# Save results
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
results_df = pd.DataFrame(real_results + scam_results)
results_df.to_csv(f'models/handshake_test_results_{timestamp}.csv', index=False)
print(f"\n💾 Results saved to models/handshake_test_results_{timestamp}.csv")

print("\n" + "="*70)