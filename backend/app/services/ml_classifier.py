"""
Machine Learning model for risk classification using transformers.
"""
import logging
from typing import Tuple
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np

logger = logging.getLogger(__name__)


class RiskClassifier:
    """ML-based risk classifier using DistilBERT for CPU inference."""
    
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        """
        Initialize the risk classifier.
        
        Args:
            model_name: Hugging Face model identifier
        """
        self.model_name = model_name
        self.device = "cpu"  # Force CPU inference
        self.classifier = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the transformer model."""
        try:
            # Use zero-shot classification for flexible risk assessment
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",  # Works well with CPU
                device=-1  # Use CPU
            )
            logger.info("Risk classifier model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ML model: {str(e)}")
            self.classifier = None
    
    def classify_risk(self, clause_text: str) -> Tuple[str, float]:
        """
        Classify the risk level of a clause.
        
        Args:
            clause_text: The clause text to classify
            
        Returns:
            Tuple of (risk_level, confidence_score)
        """
        if not self.classifier or not clause_text.strip():
            return "low", 0.5
        
        try:
            candidate_labels = ["high risk clause", "medium risk clause", "low risk clause"]
            result = self.classifier(clause_text, candidate_labels, multi_class=False)
            
            labels = result["labels"]
            scores = result["scores"]
            
            # Map labels to risk levels
            risk_mapping = {
                "high risk clause": "high",
                "medium risk clause": "medium",
                "low risk clause": "low"
            }
            
            top_label = labels[0]
            confidence = float(scores[0])
            risk_level = risk_mapping.get(top_label, "low")
            
            logger.debug(f"Classified clause with risk: {risk_level}, confidence: {confidence}")
            return risk_level, confidence
            
        except Exception as e:
            logger.error(f"Error during classification: {str(e)}")
            return "low", 0.5
    
    def batch_classify(self, clauses: list) -> list:
        """
        Classify multiple clauses.
        
        Args:
            clauses: List of clause texts
            
        Returns:
            List of (risk_level, confidence) tuples
        """
        results = []
        for clause in clauses:
            risk_level, confidence = self.classify_risk(clause)
            results.append((risk_level, confidence))
        
        return results


# Singleton instance
_classifier_instance = None


def get_risk_classifier() -> RiskClassifier:
    """Get or create the risk classifier instance."""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = RiskClassifier()
    return _classifier_instance
