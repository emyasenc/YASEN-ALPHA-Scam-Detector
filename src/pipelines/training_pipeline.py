#!/usr/bin/env python3
"""
Training Pipeline - Trains model using your existing logic
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
import logging
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.pipelines.feature_pipeline import FeaturePipeline

logger = logging.getLogger(__name__)

class TrainingPipeline:
    def __init__(self, config):
        self.config = config
        self.models_dir = Path(config['paths']['models'])
        self.model_params = config['model']['parameters']
        self.test_size = config['training']['test_size']
        self.random_state = config['training']['random_state']
        
        self.models_dir.mkdir(parents=True, exist_ok=True)
    
    def load_features(self):
        """Load precomputed features or compute fresh"""
        features_path = self.models_dir / 'X_train.npy'
        target_path = self.models_dir / 'y_train.npy'
    
        # Try to load precomputed features
        if features_path.exists() and target_path.exists():
            try:
                X = np.load(features_path, allow_pickle=True)  # Add allow_pickle=True
                y = np.load(target_path, allow_pickle=True)    # Add allow_pickle=True
                logger.info(f"📂 Loaded precomputed features: {X.shape}")
                return X, y
            except Exception as e:
                logger.warning(f"⚠️ Failed to load cached features: {e}")
                logger.info("   Regenerating features...")
                # Delete corrupted files
                features_path.unlink(missing_ok=True)
                target_path.unlink(missing_ok=True)
    
        # Otherwise compute fresh
        logger.info("🔧 Computing features...")
        feature_pipeline = FeaturePipeline(self.config)
        X, y, _ = feature_pipeline.run()
    
        # Cache for next time
        np.save(features_path, X, allow_pickle=True)
        np.save(target_path, y, allow_pickle=True)
    
        return X, y
    
    def split_data(self, X, y):
        """Split into train/test"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        logger.info(f"📊 Train: {X_train.shape}, Test: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train, y_train):
        """Train model using your parameters"""
        logger.info("🤖 Training model...")
        
        model = LogisticRegression(
            C=self.model_params['C'],
            class_weight=self.model_params['class_weight'],
            max_iter=self.model_params['max_iter'],
            random_state=self.random_state
        )
        
        model.fit(X_train, y_train)
        
        # Calculate training metrics
        train_acc = model.score(X_train, y_train)
        logger.info(f"   ✅ Training accuracy: {train_acc:.4f}")
        
        return model
    
    def save_model(self, model):
        """Save trained model"""
        model_path = self.models_dir / 'production_model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"💾 Model saved to {model_path}")
        
        # Also save threshold
        threshold_path = self.models_dir / 'threshold.txt'
        with open(threshold_path, 'w') as f:
            f.write(str(self.config['model']['threshold']))
        logger.info(f"💾 Threshold saved: {self.config['model']['threshold']}")
    
    def run(self):
        """Run full training pipeline"""
        logger.info("="*50)
        logger.info("🤖 Running Training Pipeline")
        logger.info("="*50)
        
        X, y = self.load_features()
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        model = self.train(X_train, y_train)
        self.save_model(model)
        
        # Return model and test data for evaluation
        return model, X_test, y_test