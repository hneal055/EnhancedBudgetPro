"""
EmotionEngine Module
Phase 13.1: Emotional Intelligence for Film & TV Production

Public API for emotion detection and analysis in screenplays.

Usage:
    from src.EmotionEngine import get_detector, EmotionAnalyzer, ArcTracker
    
    # Detect emotions
    detector = get_detector()
    emotions = detector.detect_emotion("I'm so happy!")
    
    # Analyze scenes
    analyzer = EmotionAnalyzer()
    scene_analysis = analyzer.analyze_scene(scene_dict)
    
    # Track character arcs
    char_arc = analyzer.analyze_character("MICHAEL", scenes)
    
    # Identify story moments
    tracker = ArcTracker()
    turning_points = tracker.identify_turning_points(char_arc)
"""

from .detector import EmotionDetector, get_detector
from .analyzer import EmotionAnalyzer
from .arc_tracker import ArcTracker

__all__ = [
    "EmotionDetector",
    "get_detector",
    "EmotionAnalyzer",
    "ArcTracker"
]

__version__ = "13.1.0"
