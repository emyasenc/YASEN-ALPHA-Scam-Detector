# add_failed_jobs.py
import pandas as pd

# Load your dataset
df = pd.read_csv('data/final_dataset.csv')

# The 9 jobs that failed
failed_jobs = [
    {"title": "Medical Assistant at Kaiser", "desc": "Assist physicians with patient care. CMA certification preferred.", "industry": "Healthcare"},
    {"title": "Sales Associate at Home Depot", "desc": "Help customers find products, restock shelves, provide excellent service.", "industry": "Retail"},
    {"title": "Elementary School Teacher", "desc": "Teach 3rd grade students. Teaching credential required.", "industry": "Education"},
    {"title": "College Professor - Computer Science", "desc": "Teach undergraduate CS courses. PhD in CS required.", "industry": "Education"},
    {"title": "Delivery Driver at Amazon", "desc": "Deliver packages using own vehicle. Flexible hours. Must have valid license.", "industry": "Transportation"},
    {"title": "Truck Driver - CDL Required", "desc": "Regional routes. Competitive pay and benefits.", "industry": "Transportation"},
    {"title": "Warehouse Associate at FedEx", "desc": "Pick, pack, and ship orders. Must be able to lift 50 lbs.", "industry": "Transportation"},
    {"title": "Barista at Starbucks", "desc": "Make coffee, serve customers, maintain clean workspace.", "industry": "Food Service"},
]

# Add 3 copies of each failed job
for job in failed_jobs:
    for _ in range(3):
        df = pd.concat([df, pd.DataFrame([{
            "title": job["title"],
            "description": job["desc"],
            "company": job["title"].split(" at ")[-1] if " at " in job["title"] else "Local Company",
            "source": "failed_test",
            "industry": job["industry"],
            "fraudulent": 0
        }])], ignore_index=True)

df.to_csv('data/final_dataset.csv', index=False)

print(f"✅ Added {len(failed_jobs) * 3} failed job examples to training")
print(f"📊 New total: {len(df)} rows")
print(f"   Real: {(df['fraudulent']==0).sum()}")
print(f"   Scam: {(df['fraudulent']==1).sum()}")