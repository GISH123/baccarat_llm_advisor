import sys
import os
import logging
from src.utils import setup_logging
from src.advisor import BaccaratLLMAdvisor
from tests.test_scenarios import run_baccarat_tests

def extract_model_name(config_path):
    base = os.path.basename(config_path)
    return os.path.splitext(base)[0].replace("llm_advisor_config_", "")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_single_advisor.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    model_name = extract_model_name(config_path)

    # ✅ Set up logging using model_name
    setup_logging(model_name=model_name)

    logging.info(f"Starting advisor for model: {model_name}")
    logging.info(f"Using config: {config_path}")

    try:
        advisor = BaccaratLLMAdvisor(config_path)
        run_baccarat_tests(advisor)
    except Exception as e:
        logging.error(f"Error in advisor for config '{config_path}': {e}")
        sys.exit(1)
