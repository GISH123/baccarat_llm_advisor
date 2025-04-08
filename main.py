import logging
import os
import subprocess

from src.utils import setup_logging

if __name__ == "__main__":

    config_dir = "config"
    config_files = [
        "llm_advisor_config_qwen.yaml",
        "llm_advisor_config_llama_3.1.yaml",
        "llm_advisor_config_mistral.yaml",
        "llm_advisor_config_gemma.yaml",
        "llm_advisor_config_velvet.yaml",
        "llm_advisor_config_deepseek.yaml"
    ]

    for config_file in config_files:
        config_path = os.path.join(config_dir, config_file)
        print(f"\n========== Running tests with config: {config_file} ==========")

        try:
            # Run each config in a fresh Python subprocess
            result = subprocess.run(
                ["python", "-m", "src.run_single_advisor", config_path],
                capture_output=True,
                text=True
            )

            # Print whatever the subprocess wrote to stdout
            print(result.stdout)

            # If the subprocess ended with an error code, log the stderr
            if result.returncode != 0:
                logging.error(f"Failed to run tests for {config_file}:\n{result.stderr}")

        except Exception as e:
            # This catches any higher-level failure in launching subprocess
            logging.error(f"Failed to run tests for {config_file}: {e}")
