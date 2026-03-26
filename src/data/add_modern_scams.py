# add_modern_scams.py
import pandas as pd

df = pd.read_csv('data/final_dataset.csv')

# ============================================
# ADD 50+ MODERN SCAM EXAMPLES
# ============================================

modern_scams = [
    # Remote work scams
    {"title": "Remote Data Entry - Immediate Start", "desc": "Work from home typing data. $25/hour. Just pay $40 for software access. Start today!"},
    {"title": "Virtual Assistant - Make $5000/month", "desc": "Be your own boss! Flexible hours. Starter kit $50. No experience needed."},
    {"title": "Remote Customer Service - No Experience", "desc": "Work from home answering calls. $20/hour. Background check fee $35."},
    {"title": "AI Training Jobs", "desc": "Train AI models from home. $30/hour. Pay $50 for training materials."},
    
    # AI/ML scams
    {"title": "ChatGPT Prompt Engineer - Make $200/hour", "desc": "No experience needed! Learn to write prompts. Course only $299. Limited spots!"},
    {"title": "AI Content Creator - Work from Home", "desc": "Create content using AI tools. Starter kit $99. Make $5000/month!"},
    {"title": "Machine Learning Engineer - Fast Track", "desc": "Become ML engineer in 2 weeks. Training $499. Guaranteed job placement!"},
    {"title": "AI Artist - No Experience", "desc": "Create AI art from home. Course $199. Make $1000/week!"},
    
    # Crypto/Investment scams
    {"title": "Cryptocurrency Investment Manager", "desc": "Manage crypto investments from home. Make $10,000/month. Training $199."},
    {"title": "Forex Trading Coach", "desc": "Learn to trade forex. Special course $499. Guaranteed 100% returns!"},
    {"title": "Stock Market Expert", "desc": "Get insider trading tips. Monthly subscription $199. Make thousands!"},
    {"title": "NFT Creator - Make Millions", "desc": "Create and sell NFTs. Course $299. Join the next big thing!"},
    
    # Career scams
    {"title": "Resume Writing Service - Guaranteed Interviews", "desc": "Professional resume writers. $199 fee. Guaranteed interviews or money back!"},
    {"title": "LinkedIn Optimization Expert", "desc": "Get your profile optimized for recruiters. $149. Get 50+ recruiter views!"},
    {"title": "Interview Coaching - Guaranteed Job", "desc": "1-on-1 coaching with hiring managers. $299. Guaranteed job placement!"},
    {"title": "Career Path Consultation", "desc": "Expert career advice. $99/hour. Find your dream job guaranteed!"},
    
    # Job offer scams
    {"title": "Job Offer - Equipment Needed", "desc": "Congratulations! You're hired. Send $200 for equipment deposit to start."},
    {"title": "Background Check Fee", "desc": "We need to run a background check. $50 fee required. Refundable after hire."},
    {"title": "Training Materials Required", "desc": "Company requires training materials. $150. Reimbursed after 30 days."},
    {"title": "Visa Processing Fee", "desc": "We'll sponsor your visa. Processing fee $500. Refundable after hire."},
    
    # Social media scams
    {"title": "Social Media Manager - Make $5000", "desc": "Manage accounts from home. Training $99. No experience needed!"},
    {"title": "Instagram Influencer Manager", "desc": "Work with influencers. Starter kit $149. Make $3000/month!"},
    {"title": "TikTok Content Creator", "desc": "Create viral content. Course $199. Earn money from home!"},
    
    # Gig economy scams
    {"title": "Uber Driver Bonus - $2000", "desc": "Get $2000 sign-on bonus. Pay $50 for background check to start."},
    {"title": "DoorDash Delivery Equipment", "desc": "Purchase delivery bag and gear for $75 to start earning immediately."},
    {"title": "Amazon Flex Driver - Guaranteed", "desc": "Make $30/hour delivering packages. Registration fee $40."},
    
    # Freelance scams
    {"title": "Freelance Writer - Make $5000/month", "desc": "Write articles from home. Starter kit $30. Work with top publications!"},
    {"title": "Graphic Designer - Work from Home", "desc": "Design logos and graphics. $30/hour. Pay $45 for software access."},
    {"title": "Web Developer - No Experience", "desc": "Build websites from home. Course $299. Make $5000/month!"},
    
    # Healthcare scam variations
    {"title": "Remote Nurse Jobs - No Experience", "desc": "Work from home as a nurse. No degree needed. Pay $50 registration fee."},
    {"title": "Medical Coding Certification - 1 Week", "desc": "Get certified in 1 week. $199 for course. Make $40/hour!"},
    {"title": "Telehealth Nurse", "desc": "Work from home. Training $99. Make $50/hour! Limited spots."},
    
    # Education scams
    {"title": "Online Degree - 90% Off", "desc": "Get your bachelor's degree in 6 months. Only $500 down payment!"},
    {"title": "Teach English Online - Guaranteed", "desc": "No degree needed. $50 for TEFL certification. Make $30/hour!"},
    {"title": "College Scholarship Scam", "desc": "We guarantee $10,000 in scholarships. Processing fee $99."},
]

# Add 2 copies of each
for scam in modern_scams:
    for _ in range(2):
        df = pd.concat([df, pd.DataFrame([{
            "title": scam["title"],
            "description": scam["desc"],
            "company": "FTC Scam Alert",
            "source": "modern_scam",
            "industry": "Scam",
            "fraudulent": 1
        }])], ignore_index=True)

print(f"✅ Added {len(modern_scams) * 2} modern scam examples")
print(f"📊 New total: {len(df)} rows")
print(f"   Real: {(df['fraudulent']==0).sum()}")
print(f"   Scam: {(df['fraudulent']==1).sum()}")
print(f"   Ratio: {(df['fraudulent']==0).sum() / (df['fraudulent']==1).sum():.1f}:1")

# Save
df.to_csv('data/final_dataset.csv', index=False)
print("\n✅ Ready to retrain!")