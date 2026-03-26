# final_fix_v2.py
import pandas as pd

df = pd.read_csv('data/final_dataset.csv')

# Add MORE examples of the problematic job types
problem_jobs = [
    # Remote jobs (add 3 more)
    {"title": "After Effects Editor", "desc": "Create looping animations for digital content. Remote position.", "industry": "Remote"},
    {"title": "Video Editor", "desc": "Edit video content for social media. Remote work.", "industry": "Remote"},
    {"title": "Motion Graphics Designer", "desc": "Create animations for web and video. Fully remote.", "industry": "Remote"},
    
    # Retail (add 3 more)
    {"title": "Store Manager at Target", "desc": "Oversee store operations, manage employees.", "industry": "Retail"},
    {"title": "Assistant Store Manager", "desc": "Support store manager with daily operations.", "industry": "Retail"},
    {"title": "Retail Store Manager", "desc": "Lead retail team, drive sales, ensure customer satisfaction.", "industry": "Retail"},
    
    # Education (add 3 more)
    {"title": "Elementary School Teacher", "desc": "Teach elementary students. Teaching credential required.", "industry": "Education"},
    {"title": "Kindergarten Teacher", "desc": "Teach kindergarten students. Early childhood education credential.", "industry": "Education"},
    {"title": "Grade School Teacher", "desc": "Teach primary grades. Teaching certification required.", "industry": "Education"},
]

# Add 3 copies of each
for job in problem_jobs:
    for _ in range(3):
        df = pd.concat([df, pd.DataFrame([{
            "title": job["title"],
            "description": job["desc"],
            "company": job["title"].split(" at ")[-1] if " at " in job["title"] else "Local Company",
            "source": "final_fix_v2",
            "industry": job["industry"],
            "fraudulent": 0
        }])], ignore_index=True)

df.to_csv('data/final_dataset.csv', index=False)

print(f"✅ Added {len(problem_jobs) * 3} more examples")
print(f"📊 New total: {len(df)} rows")
print(f"   Real: {(df['fraudulent']==0).sum()}")
print(f"   Scam: {(df['fraudulent']==1).sum()}")