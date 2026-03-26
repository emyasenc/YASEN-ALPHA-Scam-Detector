# debug_training.py
import pandas as pd
import pickle

# Check if the jobs are actually in training
train = pd.read_csv('data/final_dataset.csv')
print("🔍 Checking if jobs are in training data:")
print("-" * 50)

# Check for the failed jobs
failed_titles = ["Truck Driver - CDL Required", "Bank Teller at Wells Fargo"]

for title in failed_titles:
    found = train[train['title'].str.contains(title, na=False)]
    if len(found) > 0:
        print(f"✅ {title}: FOUND in training")
        print(f"   Description: {found.iloc[0]['description'][:100]}...")
    else:
        print(f"❌ {title}: NOT found in training!")

# Also check the test set
test = pd.read_csv('models/enterprise_test_results_20260323_181731.csv')
print("\n🔍 Checking test set:")
for title in failed_titles:
    found = test[test['title'].str.contains(title, na=False)]
    if len(found) > 0:
        print(f"   {title}: prob={found.iloc[0]['probability']:.3f}")