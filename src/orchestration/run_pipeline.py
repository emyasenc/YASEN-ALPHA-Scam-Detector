#!/usr/bin/env python3
"""
Main orchestration pipeline - Runs all stages
"""

import sys
from pathlib import Path
import argparse
import yaml
from datetime import datetime
import logging
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipelines.data_pipeline import DataPipeline
from src.pipelines.training_pipeline import TrainingPipeline

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/pipeline_{datetime.now():%Y%m%d_%H%M%S}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JobScamPipeline:
    def __init__(self, config_path="src/config/config.yaml", skip_stages=None):
        self.root_dir = Path(__file__).parent.parent.parent
        self.skip_stages = skip_stages or []
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        logger.info(f"🚀 Initializing {self.config['project']['name']} v{self.config['project']['version']}")
    
    def run(self):
        """Run full pipeline"""
        logger.info("="*60)
        logger.info(f"📅 Pipeline started: {datetime.now().isoformat()}")
        logger.info("="*60)
        
        results = {}
        
        # Stage 1: Data Pipeline
        if "data" not in self.skip_stages:
            logger.info("\n📊 STAGE 1: Data Pipeline")
            data_pipeline = DataPipeline(self.config)
            df = data_pipeline.run()
            results['data'] = {"shape": df.shape, "rows": len(df)}
        else:
            logger.info("\n⏭️ Skipping Data Pipeline")
        
        # Stage 2: Training Pipeline (includes feature engineering)
        if "training" not in self.skip_stages:
            logger.info("\n🤖 STAGE 2: Training Pipeline")
            training_pipeline = TrainingPipeline(self.config)
            model, X_test, y_test = training_pipeline.run()
            results['training'] = {"model": "production_model.pkl"}
        else:
            logger.info("\n⏭️ Skipping Training Pipeline")
        
        # Stage 3: Evaluation
        if "evaluation" not in self.skip_stages:
            logger.info("\n📈 STAGE 3: Evaluation")
            
            # Run the test script directly using subprocess
            test_script = Path(__file__).parent.parent / 'tests' / 'test_model.py'
            
            if test_script.exists():
                logger.info(f"   Running test script: {test_script}")
                try:
                    result = subprocess.run(
                        [sys.executable, str(test_script)], 
                        capture_output=True, 
                        text=True,
                        timeout=300  # 5 minute timeout
                    )
                    
                    # Print output
                    if result.stdout:
                        print(result.stdout)
                    if result.stderr:
                        print(result.stderr)
                    
                    if result.returncode == 0:
                        logger.info("   ✅ Evaluation completed successfully")
                        results['evaluation'] = {"status": "completed", "return_code": 0}
                    else:
                        logger.error(f"   ❌ Evaluation failed with code {result.returncode}")
                        results['evaluation'] = {"status": "failed", "return_code": result.returncode}
                        
                except subprocess.TimeoutExpired:
                    logger.error("   ❌ Evaluation timed out after 5 minutes")
                    results['evaluation'] = {"status": "timeout"}
                except Exception as e:
                    logger.error(f"   ❌ Error running evaluation: {e}")
                    results['evaluation'] = {"status": "error", "error": str(e)}
            else:
                logger.warning(f"   ⚠️ Test script not found at {test_script}")
                results['evaluation'] = {"status": "skipped", "reason": "test_file_not_found"}
        else:
            logger.info("\n⏭️ Skipping Evaluation")
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("✅ PIPELINE COMPLETE")
        logger.info("="*60)
        logger.info("\n📊 Summary:")
        for stage, result in results.items():
            logger.info(f"   {stage}: {result}")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Run Job Scam Detector Pipeline")
    parser.add_argument("--skip", nargs="+", choices=["data", "training", "evaluation"],
                       help="Stages to skip")
    args = parser.parse_args()
    
    pipeline = JobScamPipeline(skip_stages=args.skip)
    pipeline.run()


if __name__ == "__main__":
    main()