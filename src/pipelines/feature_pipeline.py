#!/usr/bin/env python3
"""
Feature Pipeline - Creates features from cleaned data
Uses your existing train_model.py logic
"""

import sys
from pathlib import Path
import pandas as pd
import pickle
import re
import logging
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

class FeaturePipeline:
    def __init__(self, config):
        self.config = config
        self.processed_dir = Path(config['paths']['data_processed'])
        self.models_dir = Path(config['paths']['models'])
        self.vectorizer_params = config['features']['vectorizer']
        
        self.models_dir.mkdir(parents=True, exist_ok=True)
    
    def clean_text(self, text):
        """Clean text (from your train_model.py)"""
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'http\S+|www\S+|https\S+', ' URL ', text)
        text = re.sub(r'\S+@\S+', ' EMAIL ', text)
        text = re.sub(r'\d+', ' NUMBER ', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def load_data(self):
        """Load cleaned data"""
        data_path = self.processed_dir / 'final_dataset_enterprise.csv' 
        if not data_path.exists():
            raise FileNotFoundError(f"No data found at {data_path}. Run data pipeline first.")
    
        df = pd.read_csv(data_path)
        logger.info(f"📂 Loaded {len(df)} rows")
        return df
    
    def create_features(self, df):
        """Create TF-IDF features"""
        logger.info("🔧 Creating features...")
        
        # Clean text
        df['clean_title'] = df['title'].fillna('').apply(self.clean_text)
        df['clean_description'] = df['description'].fillna('').apply(self.clean_text)
        df['text'] = df['clean_title'] + " " + df['clean_description']
        
        # Create vectorizer
        vectorizer = TfidfVectorizer(
            max_features=self.vectorizer_params['max_features'],
            stop_words=self.vectorizer_params['stop_words'],
            ngram_range=tuple(self.vectorizer_params['ngram_range']),
            min_df=self.vectorizer_params['min_df'],
            max_df=self.vectorizer_params['max_df']
        )
        
        X = vectorizer.fit_transform(df['text'])
        y = df['fraudulent'].values
        
        logger.info(f"   ✅ Created {X.shape[1]} features")
        
        return X, y, vectorizer
    
    def save(self, vectorizer):
        """Save vectorizer"""
        vectorizer_path = self.models_dir / 'vectorizer.pkl'
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
        logger.info(f"💾 Vectorizer saved to {vectorizer_path}")
    
    def run(self):
        """Run full feature pipeline"""
        logger.info("="*50)
        logger.info("🔧 Running Feature Pipeline")
        logger.info("="*50)
        
        df = self.load_data()
        X, y, vectorizer = self.create_features(df)
        self.save(vectorizer)
        
        return X, y, vectorizer