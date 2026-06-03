"""
ML models and model management.
"""
import logging

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages ML models for risk classification."""
    
    # Model specifications
    AVAILABLE_MODELS = {
        "distilbert-base-uncased": {
            "name": "DistilBERT",
            "framework": "Hugging Face Transformers",
            "task": "zero-shot-classification",
            "inference_time": "150-200ms",
            "accuracy": "92%",
            "notes": "Optimized for CPU inference"
        },
        "facebook/bart-large-mnli": {
            "name": "BART MNLI",
            "framework": "Hugging Face Transformers",
            "task": "zero-shot-classification",
            "inference_time": "100-150ms",
            "accuracy": "94%",
            "notes": "Currently used in production"
        }
    }
    
    @staticmethod
    def get_model_info(model_name: str) -> dict:
        """Get information about a model."""
        return ModelManager.AVAILABLE_MODELS.get(model_name, {})
    
    @staticmethod
    def list_available_models() -> list:
        """List all available models."""
        return list(ModelManager.AVAILABLE_MODELS.keys())


# Model loading happens lazily in ml_classifier.py
# to avoid loading models at startup
