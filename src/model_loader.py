# src/model_loader.py
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import logging

logger = logging.getLogger(__name__)

class LLMModelLoader:
    def __init__(self, model_path, use_gpu=True):
        """Initialize the model loader with a model path and GPU option."""
        self.model_path = model_path
        self.use_gpu = use_gpu
        self.device = "cuda" if torch.cuda.is_available() and use_gpu else "cpu"
        if self.device == "cpu":
            logger.warning(f"Using CPU. GPU available: {torch.cuda.is_available()}, use_gpu: {use_gpu}")
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        """Load the model and tokenizer with error handling."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            # self.model = AutoModelForCausalLM.from_pretrained(self.model_path, attn_implementation="flash_attention_2")
            # self.model = AutoModelForCausalLM.from_pretrained(self.model_path)

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype="auto"  # or torch.float16
            )

            # bnb_config = BitsAndBytesConfig(load_in_8bit=True)
            # self.model = AutoModelForCausalLM.from_pretrained(
            #     self.model_path,
            #     quantization_config=bnb_config,
            #     device_map="auto"
            # )

            self.model.to(self.device)
            logger.info(f"Model loaded successfully from {self.model_path} on {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.tokenizer = None