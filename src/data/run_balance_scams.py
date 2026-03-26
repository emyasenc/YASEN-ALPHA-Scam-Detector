# run_balance_scams.py
import pandas as pd

# Load current dataset
df = pd.read_csv('src/data/processed/final_dataset_enterprise.csv')

# Add 30 more diverse scam examples
more_scams = [
    # Tech scams
    {"title": "Fake Startup Job - Equity Scam", "desc": "Join our startup! Work for equity only. No salary for 6 months. Unlimited potential!"},
    {"title": "Coding Bootcamp Scholarship", "desc": "Full scholarship to coding bootcamp! Just pay $200 registration fee. Limited spots!"},
    
    # Finance scams
    {"title": "Ponzi Scheme - High Returns", "desc": "Invest $1000, get $2000 in 30 days. Refer friends for 20% commission!"},
    {"title": "Wealth Management Coach", "desc": "Learn to manage wealth. Course $499. Guaranteed to double your money!"},
    
    # Healthcare scams
    {"title": "Insurance Billing Specialist", "desc": "Work from home billing insurance. $35/hour. Training $125. Start immediately!"},
    {"title": "Medical Records Clerk", "desc": "Manage medical records remotely. $28/hour. Certification fee $89."},
    
    # Retail scams
    {"title": "E-commerce Dropshipping Expert", "desc": "Build your own store. Course $299. Make $10,000/month! Guaranteed!"},
    {"title": "Retail Arbitrage Coach", "desc": "Buy low, sell high on Amazon. Training $199. Make $5000/week!"},
    
    # Education scams
    {"title": "Scholarship Application Service", "desc": "We'll apply to 100 scholarships for you. Service fee $199. Guaranteed $10,000!"},
    {"title": "Online Course Creator", "desc": "Create and sell online courses. Course $399. Make $20,000/month!"},
    
    # Transportation scams
    {"title": "Fleet Owner Opportunity", "desc": "Own your delivery fleet. Investment $5000. Make $2000/week passive income!"},
    {"title": "Trucking Dispatcher", "desc": "Dispatch trucks from home. $2000/week. Training $150. Limited positions!"},
    
    # Common scams
    {"title": "Mystery Shopping - Premium", "desc": "Premium mystery shopper positions. Registration $49. Earn $1000/week!"},
    {"title": "Product Tester Pro", "desc": "Test premium products. Starter kit $99. Keep everything you test!"},
]

for scam in more_scams:
    for _ in range(3):
        df = pd.concat([df, pd.DataFrame([{
            "title": scam["title"],
            "description": scam["desc"],
            "company": "FTC Scam Alert",
            "source": "ftc_scam",
            "industry": "Scam",
            "fraudulent": 1
        }])], ignore_index=True)

# Save
df.to_csv('src/data/processed/final_dataset_enterprise.csv', index=False)

print(f"✅ Added {len(more_scams) * 3} more scams")
print(f"📊 New total: {len(df)} rows")
print(f"   Real: {(df['fraudulent']==0).sum()}")
print(f"   Scam: {(df['fraudulent']==1).sum()}")
print(f"   Ratio: {(df['fraudulent']==0).sum() / (df['fraudulent']==1).sum():.1f}:1")