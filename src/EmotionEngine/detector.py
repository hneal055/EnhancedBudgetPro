"""
EmotionEngine Detector Module
Phase 13.1: HuggingFace Transformers Integration

Detects 7 core emotions in script dialogue using pre-trained model:
- joy, sadness, anger, fear, surprise, disgust, neutral

Model: j-hartmann/emotion-english-distilroberta-base
"""

from transformers import pipeline
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class EmotionDetector:
    """Detects emotions in script dialogue using HuggingFace transformers."""
    
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        """
        Initialize the emotion detection pipeline.
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self._pipeline = None
        logger.info(f"EmotionDetector initialized with model: {model_name}")
    
    @property
    def pipeline(self):
        """Lazy-load the model pipeline (saves memory until first use)."""
        if self._pipeline is None:
            logger.info(f"Loading emotion detection model: {self.model_name}")
            self._pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                top_k=None  # Return all emotion scores
            )
            logger.info("Model loaded successfully")
        return self._pipeline
    
    def detect_emotion(self, text: str) -> Dict[str, float]:
        """
        Detect emotions in a single text snippet.
        
        Args:
            text: Dialogue or action line from script
            
        Returns:
            Dict mapping emotion labels to confidence scores
            Example: {"joy": 0.85, "sadness": 0.10, ...}
        """
        if not text or not text.strip():
            return self._empty_emotion_dict()
        
        try:
            # Get all emotion scores from model
            results = self.pipeline(text[:512])[0]  # Truncate to model's max length
            
            # Convert list of dicts to single dict
            emotion_scores = {item['label']: item['score'] for item in results}
            
            return emotion_scores
            
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return self._empty_emotion_dict()
    
    def detect_batch(self, texts: List[str], batch_size: int = 8) -> List[Dict[str, float]]:
        """
        Detect emotions for multiple texts efficiently (batched processing).
        
        Args:
            texts: List of dialogue/action lines
            batch_size: Number of texts to process per batch
            
        Returns:
            List of emotion score dictionaries
        """
        if not texts:
            return []
        
        # Filter empty texts and truncate
        valid_texts = [t[:512] for t in texts if t and t.strip()]
        
        if not valid_texts:
            return [self._empty_emotion_dict()] * len(texts)
        
        try:
            # Batch process all texts
            results = self.pipeline(valid_texts, batch_size=batch_size, truncation=True)
            
            # Convert results to list of dicts
            emotion_dicts = []
            for result_list in results:
                emotion_scores = {item['label']: item['score'] for item in result_list}
                emotion_dicts.append(emotion_scores)
            
            return emotion_dicts
            
        except Exception as e:
            logger.error(f"Error in batch emotion detection: {e}")
            return [self._empty_emotion_dict()] * len(texts)
    
    def get_dominant_emotion(self, emotion_scores: Dict[str, float]) -> str:
        """
        Get the emotion with highest confidence score.
        
        Args:
            emotion_scores: Dict of emotion->score mappings
            
        Returns:
            Emotion label with highest score (e.g., "joy")
        """
        if not emotion_scores:
            return "neutral"
        
        return max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    def _empty_emotion_dict(self) -> Dict[str, float]:
        """Return neutral emotion scores."""
        return {
            "anger": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "joy": 0.0,
            "neutral": 1.0,
            "sadness": 0.0,
            "surprise": 0.0
        }


# Global singleton instance (lazy-loaded)
_detector_instance: Optional[EmotionDetector] = None


def get_detector() -> EmotionDetector:
    """
    Get global EmotionDetector instance (singleton pattern).
    
    Returns:
        Shared EmotionDetector instance
    """
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = EmotionDetector()
    return _detector_instance
