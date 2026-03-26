"""
Enhanced test on REAL LinkedIn job posts - 30+ diverse jobs
"""

import pickle
import pandas as pd
import re
from datetime import datetime

print("="*70)
print("🔍 ENHANCED REAL LINKEDIN JOB TEST SUITE")
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
# ENHANCED REAL LINKEDIN JOB POSTS (30+ jobs)
# ============================================

linkedin_jobs = [
    # Technology (5 jobs)
    {"title": "Senior Software Engineer", "company": "Google", "desc": "Design and build scalable backend systems. 5+ years experience in Java, Python, or Go. BS in CS required.", "expected": "REAL"},
    {"title": "Frontend Developer", "company": "Meta", "desc": "Build responsive web applications with React. 3+ years experience with JavaScript, React.", "expected": "REAL"},
    {"title": "DevOps Engineer", "company": "Amazon AWS", "desc": "Manage cloud infrastructure with Kubernetes, Docker. 4+ years AWS experience.", "expected": "REAL"},
    {"title": "Data Scientist", "company": "Microsoft", "desc": "Develop ML models using Python, TensorFlow. PhD or MS in CS/Statistics.", "expected": "REAL"},
    {"title": "Product Manager", "company": "Apple", "desc": "Lead product development for iOS. 4+ years product management experience.", "expected": "REAL"},
    
    # Healthcare (5 jobs)
    {"title": "Registered Nurse - ICU", "company": "Mayo Clinic", "desc": "Provide critical care. RN license required. 2+ years ICU experience.", "expected": "REAL"},
    {"title": "Medical Assistant", "company": "Kaiser Permanente", "desc": "Assist physicians with patient care. CMA certification preferred.", "expected": "REAL"},
    {"title": "Physical Therapist", "company": "Cleveland Clinic", "desc": "Develop treatment plans. DPT and state license required.", "expected": "REAL"},
    {"title": "Pharmacist", "company": "CVS Health", "desc": "Dispense medications, counsel patients. PharmD required.", "expected": "REAL"},
    {"title": "Dental Hygienist", "company": "Aspen Dental", "desc": "Clean teeth, educate patients. RDH license required.", "expected": "REAL"},
    
    # Finance (3 jobs)
    {"title": "Financial Analyst", "company": "JPMorgan Chase", "desc": "Analyze financial data, create models. 2+ years experience.", "expected": "REAL"},
    {"title": "Accountant", "company": "Deloitte", "desc": "Prepare financial statements, handle tax filings. CPA preferred.", "expected": "REAL"},
    {"title": "Bank Teller", "company": "Wells Fargo", "desc": "Process transactions, assist customers. Cash handling experience.", "expected": "REAL"},
    
    # Education (3 jobs)
    {"title": "High School Math Teacher", "company": "LAUSD", "desc": "Teach algebra and calculus. Teaching credential required.", "expected": "REAL"},
    {"title": "Elementary Teacher", "company": "NYC DOE", "desc": "Teach 3rd grade. Teaching credential required.", "expected": "REAL"},
    {"title": "College Professor", "company": "Stanford", "desc": "Teach computer science. PhD required.", "expected": "REAL"},
    
    # Retail (3 jobs)
    {"title": "Store Manager", "company": "Target", "desc": "Oversee store operations, manage 50+ employees.", "expected": "REAL"},
    {"title": "Cashier", "company": "Walmart", "desc": "Process transactions, assist customers.", "expected": "REAL"},
    {"title": "Sales Associate", "company": "Home Depot", "desc": "Help customers find products, restock shelves.", "expected": "REAL"},
    
    # Food Service (3 jobs)
    {"title": "Restaurant Manager", "company": "Olive Garden", "desc": "Manage daily operations, train staff.", "expected": "REAL"},
    {"title": "Line Cook", "company": "Chipotle", "desc": "Prepare fresh ingredients, cook to order.", "expected": "REAL"},
    {"title": "Barista", "company": "Starbucks", "desc": "Make coffee, serve customers, maintain clean workspace.", "expected": "REAL"},
    
    # Transportation (3 jobs)
    {"title": "Delivery Driver", "company": "Amazon", "desc": "Deliver packages. Valid license required. $18-22/hour.", "expected": "REAL"},
    {"title": "Truck Driver", "company": "UPS", "desc": "CDL required. Regional routes. Competitive pay.", "expected": "REAL"},
    {"title": "Warehouse Associate", "company": "FedEx", "desc": "Pick, pack, ship orders. Must lift 50 lbs.", "expected": "REAL"},
    
    # Construction (3 jobs)
    {"title": "Electrician", "company": "Bechtel", "desc": "Install and repair electrical systems. Journeyman license.", "expected": "REAL"},
    {"title": "Carpenter", "company": "Turner Construction", "desc": "Frame buildings, install fixtures. 3+ years experience.", "expected": "REAL"},
    {"title": "Plumber", "company": "Ferguson", "desc": "Install and repair plumbing systems. Licensed plumber.", "expected": "REAL"},
    
    # Hospitality (2 jobs)
    {"title": "Hotel Manager", "company": "Marriott", "desc": "Oversee hotel operations, manage staff.", "expected": "REAL"},
    {"title": "Front Desk Agent", "company": "Hilton", "desc": "Check guests in/out, provide excellent service.", "expected": "REAL"},
    
    # Administrative (2 jobs)
    {"title": "Administrative Assistant", "company": "Robert Half", "desc": "Support executives with scheduling, communications.", "expected": "REAL"},
    {"title": "Executive Assistant", "company": "Adecco", "desc": "Manage calendars, arrange travel, prepare documents.", "expected": "REAL"},
]

# ============================================
# ENHANCED SCAM EXAMPLES (15 scams)
# ============================================

scam_jobs = [
    {"title": "WORK FROM HOME - MAKE $5000/WEEK!!!", "desc": "No experience needed! Send $50 for training materials.", "expected": "SCAM"},
    {"title": "Urgent: Bank Details Needed", "desc": "Send bank account and SSN to verify.", "expected": "SCAM"},
    {"title": "Mystery Shopper - EASY MONEY!", "desc": "Wire $99 for registration fee.", "expected": "SCAM"},
    {"title": "Data Entry - Make $5000 Monthly", "desc": "Pay $25 registration fee.", "expected": "SCAM"},
    {"title": "AI Prompt Engineer - Make $200/hour", "desc": "Course $299. Guaranteed job placement!", "expected": "SCAM"},
    {"title": "ChatGPT Expert Needed", "desc": "Training $199. Make $5000/month.", "expected": "SCAM"},
    {"title": "Cryptocurrency Trader", "desc": "500% returns. Investment $500. Training $299.", "expected": "SCAM"},
    {"title": "Medical Billing Training", "desc": "Certified in 2 weeks. $199. Make $40/hour!", "expected": "SCAM"},
    {"title": "Remote Nurse Jobs", "desc": "Work from home. Pay $50 registration fee.", "expected": "SCAM"},
    {"title": "Fake Google Job", "desc": "Pay $50 for background check to schedule interview.", "expected": "SCAM"},
    {"title": "Bitcoin Investment", "desc": "Double your money in 30 days. Minimum $1000.", "expected": "SCAM"},
    {"title": "Forex Trading Signals", "desc": "90% accurate. $199/month. Make thousands!", "expected": "SCAM"},
    {"title": "Teacher Certification Fast Track", "desc": "Get certified in 2 weeks. $299 for materials.", "expected": "SCAM"},
    {"title": "Online Degree - 90% Off", "desc": "Bachelor's in 6 months. $500 down payment.", "expected": "SCAM"},
    {"title": "Package Reshipper Needed", "desc": "Receive and reship packages. $1000/week.", "expected": "SCAM"},
]

# ============================================
# RUN PREDICTIONS
# ============================================

print("\n" + "="*70)
print(f"📊 TESTING {len(linkedin_jobs)} REAL JOBS + {len(scam_jobs)} SCAMS")
print("="*70)

# Test real jobs
print("\n✅ REAL JOBS (Should be REAL):")
print("-" * 70)

real_results = []
for job in linkedin_jobs:
    text = clean_text(job["title"]) + " " + clean_text(job["desc"])
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
    
    if not is_scam:
        print(f"✅ REAL: {job['title']} at {job['company']} (prob: {prob:.3f})")
    else:
        print(f"❌ SCAM: {job['title']} at {job['company']} (prob: {prob:.3f})")

# Test scam jobs
print("\n\n🚨 SCAM JOBS (Should be SCAM):")
print("-" * 70)

scam_results = []
for job in scam_jobs:
    text = clean_text(job["title"]) + " " + clean_text(job["desc"])
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
total = len(linkedin_jobs) + len(scam_jobs)

print(f"\n✅ Real Jobs: {real_passed}/{len(linkedin_jobs)} correct ({real_passed/len(linkedin_jobs)*100:.1f}%)")
print(f"✅ Scam Jobs: {scam_passed}/{len(scam_jobs)} correct ({scam_passed/len(scam_jobs)*100:.1f}%)")
print(f"✅ Total: {real_passed + scam_passed}/{total} correct ({((real_passed + scam_passed)/total * 100):.1f}%)")

# Show failures
if real_passed < len(linkedin_jobs):
    print("\n❌ FAILED REAL JOBS:")
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

if real_passed >= len(linkedin_jobs) * 0.95 and scam_passed == len(scam_jobs):
    print("\n🏆 EXCELLENT! 95%+ real job accuracy, 100% scam detection.")
    print("✅ READY FOR ENTERPRISE DEPLOYMENT!")
elif real_passed >= len(linkedin_jobs) * 0.9 and scam_passed >= len(scam_jobs) * 0.95:
    print("\n✅ GOOD! Ready for production deployment.")
elif real_passed >= len(linkedin_jobs) * 0.8:
    print("\n⚠️ ACCEPTABLE. Deploy with monitoring. Add failures to training.")
else:
    print("\n❌ NEEDS IMPROVEMENT. Add failures to training and retrain.")

# Save results
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
results_df = pd.DataFrame(real_results + scam_results)
results_df.to_csv(f'models/linkedin_test_enhanced_{timestamp}.csv', index=False)
print(f"\n💾 Results saved to models/linkedin_test_enhanced_{timestamp}.csv")

print("\n" + "="*70)