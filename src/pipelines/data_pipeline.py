#!/usr/bin/env python3
"""
Data Pipeline - Collects, cleans, validates, and BALANCES job data
Now includes automatic scam balancing after data collection
"""

import sys
from pathlib import Path
import pandas as pd
import logging
import yaml
from datetime import datetime
import importlib.util

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

class DataPipeline:
    def __init__(self, config):
        self.config = config
        self.raw_dir = Path(config['paths']['data_raw'])
        self.processed_dir = Path(config['paths']['data_processed'])
        
        # Create directories
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Target ratio for balancing (aim for 4:1 to 5:1)
        self.target_ratio = 4.5  # Aim for ~4.5 real jobs per scam
    
    def collect(self):
        """Collect data by running build_dataset.py and loading the result"""
        logger.info("📡 Collecting jobs from sources...")
        
        # Import and run build_dataset.py to generate the data
        build_dataset_path = Path(__file__).parent.parent / 'data' / 'build_dataset.py'
        
        # Execute build_dataset.py to create the dataset
        import subprocess
        result = subprocess.run([sys.executable, str(build_dataset_path)], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Build dataset failed: {result.stderr}")
            raise RuntimeError("Failed to build dataset")
        
        # Load the generated dataset
        data_path = self.processed_dir / 'final_dataset_enterprise.csv'
        if not data_path.exists():
            raise FileNotFoundError(f"No data found at {data_path}")
        
        df = pd.read_csv(data_path)
        logger.info(f"   ✅ Loaded {len(df)} jobs from dataset")
        return df
    
    def clean(self, df):
        """Clean and validate data"""
        logger.info("🧹 Cleaning data...")
        
        # Remove duplicates
        before = len(df)
        df = df.drop_duplicates(subset=['title', 'description'])
        logger.info(f"   Removed {before - len(df)} duplicates")
        
        # Remove rows with empty descriptions
        before = len(df)
        df = df[df['description'].str.len() > 50]
        logger.info(f"   Removed {before - len(df)} rows with short descriptions")
        
        # Add timestamp
        df['collected_date'] = datetime.now().isoformat()
        
        return df
    
    def balance_dataset(self, df):
        """Balance the dataset by adding scam examples if needed"""
        logger.info("⚖️ Checking dataset balance...")
        
        real_count = (df['fraudulent'] == 0).sum()
        scam_count = (df['fraudulent'] == 1).sum()
        current_ratio = real_count / scam_count if scam_count > 0 else float('inf')
        
        logger.info(f"   Current ratio: {current_ratio:.1f}:1 ({real_count} real, {scam_count} scam)")
        
        if current_ratio <= self.target_ratio:
            logger.info(f"   ✅ Ratio is good (target: {self.target_ratio}:1)")
            return df
        
        # Need to add more scams
        needed_scams = int(real_count / self.target_ratio) - scam_count
        logger.info(f"   ⚠️ Need ~{needed_scams} more scam examples to reach {self.target_ratio}:1")
        
        # Add dynamic scam examples based on current dataset
        df = self._add_balanced_scams(df, needed_scams)
        
        new_real = (df['fraudulent'] == 0).sum()
        new_scam = (df['fraudulent'] == 1).sum()
        new_ratio = new_real / new_scam
        
        logger.info(f"   ✅ After balancing: {new_ratio:.1f}:1 ({new_real} real, {new_scam} scam)")
        
        return df
    
    def _add_balanced_scams(self, df, needed_scams):
        """Add scam examples based on current dataset size"""
        
        # Base scam templates
        scam_templates = [
            # Tech scams
            {"title": "Fake Google Job - Pay for Interview", "desc": "We need $50 for background check to schedule your Google interview. Limited slots!"},
            {"title": "Remote Amazon Job - Training Required", "desc": "Work from home for Amazon. Pay $75 for training materials. Start today!"},
            {"title": "Microsoft Data Entry", "desc": "Microsoft is hiring data entry. $30/hour. Registration fee $40."},
            {"title": "Facebook Moderator", "desc": "Work from home moderating content. Pay $50 for certification. Earn $25/hour."},
            {"title": "Apple Support Agent", "desc": "Provide Apple support from home. Training fee $60. Immediate hiring!"},
            {"title": "Netflix Tester", "desc": "Test Netflix content. $100/week. Registration fee $25."},
            {"title": "Tesla Remote Job", "desc": "Work for Tesla from home. $35/hour. Pay $100 for equipment deposit."},
            
            # Finance scams
            {"title": "Bitcoin Investment - 500% Returns", "desc": "Double your money in 30 days. Minimum investment $1000. Guaranteed!"},
            {"title": "Forex Trading Signals", "desc": "Get 90% accurate trading signals. Only $199/month. Make thousands!"},
            {"title": "Credit Repair Specialist", "desc": "Become certified. $299 for materials. Make $5000/month!"},
            {"title": "Cryptocurrency Mining", "desc": "Mine Bitcoin from home. Starter kit $199. Make $5000/month!"},
            {"title": "NFT Investment", "desc": "Guaranteed 200% returns on NFT investments. Minimum $500."},
            
            # Healthcare scams
            {"title": "Medical Coding Certification", "desc": "Get certified in 1 week. $199 for course. Make $40/hour!"},
            {"title": "Nursing Assistant Training", "desc": "Become CNA in 2 weeks. $150 for materials. Guaranteed job!"},
            {"title": "Pharmacy Technician", "desc": "Online certification. $99 for study materials. Start your career!"},
            {"title": "Remote Nurse Jobs", "desc": "Work from home as a nurse. No experience needed. Pay $50 registration fee."},
            {"title": "Medical Billing Training", "desc": "Become a certified medical biller in 2 weeks. Training only $199. Make $50/hour!"},
            
            # Retail scams
            {"title": "Amazon Product Tester", "desc": "Get free products. Pay $25 for starter kit. Make $1000/month!"},
            {"title": "Walmart Mystery Shopper", "desc": "Shop and get paid. Registration fee $30. Earn $500/week!"},
            {"title": "Target Gift Card Tester", "desc": "Test gift cards from home. $20 fee. Keep what you test!"},
            {"title": "Retail Inventory Specialist", "desc": "Work from home counting inventory. $30/hour. Pay $50 for training materials."},
            
            # Education scams
            {"title": "Teach English Online - Guaranteed", "desc": "No degree needed. $50 for TEFL certification. Make $30/hour!"},
            {"title": "Online Degree - 90% Off", "desc": "Get your bachelor's degree in 6 months. Only $500 down payment!"},
            {"title": "College Scholarship Scam", "desc": "We guarantee $10,000 in scholarships. Processing fee $99."},
            {"title": "Teacher Certification - Fast Track", "desc": "Get certified in 2 weeks. $299 for materials. Guaranteed job placement!"},
            
            # Common scams
            {"title": "Data Entry - Work From Home", "desc": "Earn $5000/month typing. No experience needed. Just $30 registration fee."},
            {"title": "Virtual Assistant - Immediate Start", "desc": "Be your own boss! Make $4000/month. Starter kit $50."},
            {"title": "Package Reshipper Needed", "desc": "Receive and reship packages from home. $1000/week. No experience needed."},
            {"title": "Career Coach - Guaranteed Job", "desc": "Pay $500 for coaching program. 100% job placement guarantee!"},
            {"title": "Customer Service - Remote", "desc": "Work from home answering calls. $20/hour. Background check fee $35."},
        ]
        
        import random
        added = 0
        
        while added < needed_scams and added < 100:
            for scam in scam_templates:
                if added >= needed_scams:
                    break
                copies = random.randint(1, 3)
                for _ in range(copies):
                    if added >= needed_scams:
                        break
                    df = pd.concat([df, pd.DataFrame([{
                        "title": scam["title"],
                        "description": scam["desc"],
                        "company": "FTC Scam Alert",
                        "source": "ftc_scam",
                        "industry": "Scam",
                        "fraudulent": 1
                    }])], ignore_index=True)
                    added += 1
        
        logger.info(f"   ✅ Added {added} scam examples")
        return df
    
    def save(self, df):
        """Save processed data"""
        output_path = self.processed_dir / 'final_dataset_enterprise.csv'
        df.to_csv(output_path, index=False)
        logger.info(f"💾 Saved to {output_path}")
        return output_path
    
    def run(self):
        """Run full data pipeline with balancing"""
        logger.info("="*50)
        logger.info("🚀 Running Data Pipeline (with Auto-Balancing)")
        logger.info("="*50)
        
        # Collect (this runs build_dataset.py)
        df = self.collect()
        
        # Clean
        df = self.clean(df)
        
        # Augment with existing data (if exists and not already loaded)
        # The collect() already loads the latest data, so no need to augment again
        
        # Balance the dataset (add scams if needed)
        df = self.balance_dataset(df)
        
        # Save
        self.save(df)
        
        return df