"""
EmotionEngine Detector Module
Phase 13.1: HuggingFace Transformers Integration
Phase 13.3: Batch Processing & Caching
Phase 13.6: GPU/CUDA Acceleration

Detects 7 core emotions in script dialogue using pre-trained model:
- joy, sadness, anger, fear, surprise, disgust, neutral

Model: j-hartmann/emotion-english-distilroberta-base

PERFORMANCE OPTIMIZATIONS:
- Phase 13.3: Streamlit caching, 32 text batches
- Phase 13.6: CUDA GPU acceleration (5-10x faster)

GPU Strategy:
- Auto-detects CUDA GPU if available
- Falls back to CPU gracefully
- Supports manual device override
- Logs device selection for transparency
"""

from transformers import pipeline
from typing import Dict, List, Optional
import logging
import time
import torch

logger = logging.getLogger(__name__)


class EmotionDetector:
    """Detects emotions in script dialogue using HuggingFace transformers."""
    
    def __init__(
        self, 
        model_name: str = "j-hartmann/emotion-english-distilroberta-base",
        device: Optional[str] = None
    ):
        """
        Initialize the emotion detection pipeline.
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to use ('cuda', 'cpu', or None for auto-detect)
                   None = auto-detect GPU, fallback to CPU
                   'cuda' = force GPU (error if unavailable)
                   'cpu' = force CPU
        """
        self.model_name = model_name
        self._pipeline = None
        self._load_time = None
        self._device = self._select_device(device)
        logger.info(f"EmotionDetector initialized with model: {model_name}")
        logger.info(f"Target device: {self._device}")
    
    def _select_device(self, device: Optional[str] = None) -> str:
        """
        Select compute device (GPU or CPU).
        
        Args:
            device: User-specified device or None for auto-detect
            
        Returns:
            Device string ('cuda' or 'cpu')
        """
        if device is not None:
            # Manual override
            if device == 'cuda' and not torch.cuda.is_available():
                logger.error("CUDA GPU requested but not available! Falling back to CPU.")
                return 'cpu'
            return device
        
        # Auto-detect: Use GPU if available
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            logger.info(f"🚀 GPU detected: {gpu_name} ({gpu_memory:.1f} GB)")
            logger.info("   Enabling CUDA acceleration (5-10x faster expected)")
            return 'cuda'
        else:
            logger.info("ℹ️  No GPU detected, using CPU")
            logger.info("   For GPU acceleration, install CUDA-enabled PyTorch:")
            logger.info("   pip install torch --index-url https://download.pytorch.org/whl/cu118")
            return 'cpu'
    
    @property
    def device(self) -> str:
        """Get current compute device."""
        return self._device
    
    @property
    def is_gpu_enabled(self) -> bool:
        """Check if GPU acceleration is active."""
        return self._device == 'cuda'
    
    @property
    def pipeline(self):
        """Lazy-load the model pipeline (saves memory until first use)."""
        if self._pipeline is None:
            start = time.time()
            logger.info(f"Loading emotion detection model: {self.model_name}")
            logger.info(f"Device: {self._device}")
            
            # Convert device string to int for pipeline (0 = first GPU, -1 = CPU)
            device_id = 0 if self._device == 'cuda' else -1
            
            self._pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                device=device_id,  # GPU: 0, CPU: -1
                top_k=None  # Return all emotion scores
            )
            self._load_time = time.time() - start
            
            actual_device = "GPU (CUDA)" if self._device == 'cuda' else "CPU"
            logger.info(f"✅ Model loaded on {actual_device} in {self._load_time:.2f}s")
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
    
    def detect_batch(
        self, 
        texts: List[str], 
        batch_size: int = 32,  # Increased from 8 for better performance
        progress_callback=None
    ) -> List[Dict[str, float]]:
        """
        Detect emotions for multiple texts efficiently (batched processing).
        
        Args:
            texts: List of dialogue/action lines
            batch_size: Number of texts to process per batch (default 32)
            progress_callback: Optional callback(current, total) for progress tracking
            
        Returns:
            List of emotion score dictionaries
        """
        if not texts:
            return []
        
        start_time = time.time()
        
        # Filter empty texts and truncate
        valid_texts = [t[:512] for t in texts if t and t.strip()]
        
        if not valid_texts:
            return [self._empty_emotion_dict()] * len(texts)
        
        try:
            # Batch process all texts with progress tracking
            results = []
            total_batches = (len(valid_texts) + batch_size - 1) // batch_size
            
            for i in range(0, len(valid_texts), batch_size):
                batch = valid_texts[i:i+batch_size]
                batch_results = self.pipeline(batch, batch_size=batch_size, truncation=True)
                results.extend(batch_results)
                
                # Call progress callback if provided
                if progress_callback:
                    current_batch = (i // batch_size) + 1
                    progress_callback(current_batch, total_batches)
            
            # Convert results to list of dicts
            emotion_dicts = []
            for result_list in results:
                emotion_scores = {item['label']: item['score'] for item in result_list}
                emotion_dicts.append(emotion_scores)
            
            elapsed = time.time() - start_time
            throughput = len(valid_texts) / elapsed
            device_label = "GPU" if self.is_gpu_enabled else "CPU"
            logger.info(f"Batch processed {len(valid_texts)} texts on {device_label} in {elapsed:.2f}s ({throughput:.1f} texts/sec)")
            
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
    
    def get_load_time(self) -> Optional[float]:
        """Return model load time in seconds, or None if not loaded yet."""
        return self._load_time
    
    def get_device_info(self) -> Dict[str, any]:
        """
        Get detailed device information.
        
        Returns:
            Dict with device details (type, name, memory, etc.)
        """
        info = {
            'device': self._device,
            'is_gpu': self.is_gpu_enabled,
            'cuda_available': torch.cuda.is_available(),
        }
        
        if self.is_gpu_enabled and torch.cuda.is_available():
            info['gpu_name'] = torch.cuda.get_device_name(0)
            info['gpu_memory_gb'] = torch.cuda.get_device_properties(0).total_memory / 1e9
            info['pytorch_cuda_version'] = torch.version.cuda
        
        return info


# Global singleton instance (lazy-loaded)
_detector_instance: Optional[EmotionDetector] = None


def get_detector(device: Optional[str] = None) -> EmotionDetector:
    """
    Get global EmotionDetector instance (singleton pattern).
    
    Args:
        device: Device override ('cuda', 'cpu', or None for auto)
    
    Returns:
        Shared EmotionDetector instance
    """
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = EmotionDetector(device=device)
    return _detector_instance


# Streamlit caching wrapper (Phase 13.3 Performance Optimization)
def get_cached_detector(device: Optional[str] = None):
    """
    Get Streamlit-cached EmotionDetector instance.
    
    IMPORTANT: Import streamlit at call time to avoid import errors in CLI/Flask.
    This function should ONLY be called from Streamlit pages.
    
    Args:
        device: Device override ('cuda', 'cpu', or None for auto)
    
    Returns:
        Cached EmotionDetector instance (persists across Streamlit reruns)
    """
    try:
        import streamlit as st
        
        @st.cache_resource
        def _load_detector():
            """Streamlit cached detector - persists across all sessions."""
            detector = EmotionDetector(device=device)
            # Pre-load the model by accessing pipeline property
            _ = detector.pipeline
            logger.info("EmotionDetector cached in Streamlit resource cache")
            return detector
        
        return _load_detector()
    except ImportError:
        # Fallback to regular singleton if not in Streamlit context
        logger.warning("Streamlit not available, using standard singleton detector")
        return get_detector(device=device)
