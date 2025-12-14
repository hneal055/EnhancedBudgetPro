"""
Character Consistency Analyzer
Detects out-of-character moments and behavior pattern deviations
"""

from typing import Dict, List, Tuple
from collections import Counter


class ConsistencyAnalyzer:
    """
    Analyzes character behavior consistency across scenes.
    
    Features:
    - Detect out-of-character emotional moments
    - Identify behavior pattern deviations
    - Calculate consistency scores
    - Generate confidence warnings
    """
    
    def analyze_consistency(self, character_name: str, character_arc: Dict) -> Dict:
        """
        Analyze character's emotional consistency.
        
        Returns:
        {
            "character": str,
            "consistency_score": float,  # 0-100
            "baseline_emotions": [str],
            "deviations": [dict],
            "pattern_analysis": str,
            "warnings": [str],
            "confidence": float
        }
        """
        emotions_by_scene = character_arc.get("emotions_by_scene", {})
        
        if len(emotions_by_scene) < 3:
            return {
                "character": character_name,
                "consistency_score": 0.0,
                "baseline_emotions": [],
                "deviations": [],
                "pattern_analysis": "Insufficient data (need 3+ scenes)",
                "warnings": ["Need at least 3 scenes to analyze consistency"],
                "confidence": 0.0
            }
        
        # Extract emotion sequence
        scene_indices = sorted(emotions_by_scene.keys())
        emotions = [emotions_by_scene[idx].get("emotion", "neutral") for idx in scene_indices]
        intensities = [emotions_by_scene[idx].get("intensity", 0.5) for idx in scene_indices]
        
        # Determine baseline emotions (most common patterns)
        baseline_emotions = self._calculate_baseline(emotions)
        
        # Detect deviations from baseline
        deviations = self._detect_deviations(
            scene_indices, 
            emotions, 
            intensities,
            baseline_emotions
        )
        
        # Calculate consistency score
        consistency_score = self._calculate_consistency_score(emotions, deviations)
        
        # Analyze behavior patterns
        pattern_analysis = self._analyze_patterns(emotions, baseline_emotions)
        
        # Generate warnings
        warnings = self._generate_warnings(deviations, consistency_score, len(emotions))
        
        # Calculate confidence
        confidence = min(len(emotions) / 5.0, 1.0)  # More scenes = higher confidence
        
        return {
            "character": character_name,
            "consistency_score": round(consistency_score, 1),
            "baseline_emotions": baseline_emotions,
            "deviations": deviations,
            "pattern_analysis": pattern_analysis,
            "warnings": warnings,
            "confidence": round(confidence, 2)
        }
    
    def _calculate_baseline(self, emotions: List[str]) -> List[str]:
        """Calculate character's baseline emotional patterns."""
        # Count emotion frequencies
        emotion_counts = Counter(emotions)
        
        # Get top 2-3 most common emotions (baseline)
        total = len(emotions)
        baseline = []
        
        for emotion, count in emotion_counts.most_common():
            if count / total >= 0.2:  # At least 20% frequency
                baseline.append(emotion)
            if len(baseline) >= 3:
                break
        
        return baseline if baseline else [emotion_counts.most_common(1)[0][0]]
    
    def _detect_deviations(
        self, 
        scenes: List[int],
        emotions: List[str],
        intensities: List[float],
        baseline: List[str]
    ) -> List[Dict]:
        """Detect out-of-character moments."""
        deviations = []
        
        # Emotional opposites
        opposites = {
            "joy": ["sadness", "anger", "fear"],
            "sadness": ["joy"],
            "anger": ["joy"],
            "fear": ["joy"],
            "surprise": [],  # Surprise can go either way
            "neutral": []
        }
        
        for i, emotion in enumerate(emotions):
            scene_idx = scenes[i]
            intensity = intensities[i]
            
            # Check if emotion is drastically different from baseline
            if baseline:
                primary_baseline = baseline[0]
                
                # Deviation if emotion is opposite of primary baseline
                if emotion in opposites.get(primary_baseline, []):
                    severity = self._calculate_severity(emotion, intensity, baseline, i, len(emotions))
                    
                    deviations.append({
                        "scene": scene_idx,
                        "emotion": emotion,
                        "intensity": round(intensity, 2),
                        "expected": primary_baseline,
                        "severity": severity,
                        "description": self._describe_deviation(emotion, primary_baseline, severity)
                    })
                
                # Also flag sudden high-intensity shifts
                if i > 0:
                    prev_intensity = intensities[i-1]
                    intensity_jump = abs(intensity - prev_intensity)
                    
                    if intensity_jump > 0.4 and emotion not in baseline:
                        deviations.append({
                            "scene": scene_idx,
                            "emotion": emotion,
                            "intensity": round(intensity, 2),
                            "expected": "gradual change",
                            "severity": "moderate",
                            "description": f"Sudden intensity jump ({intensity_jump:.1f}) to {emotion}"
                        })
        
        return deviations
    
    def _calculate_severity(
        self, 
        emotion: str, 
        intensity: float,
        baseline: List[str],
        position: int,
        total_scenes: int
    ) -> str:
        """Calculate deviation severity level."""
        # High intensity + opposite emotion = severe
        if intensity > 0.7:
            return "severe"
        
        # Mid-story deviation more surprising
        if 0.3 < position / total_scenes < 0.7:
            return "moderate"
        
        # Low intensity or early/late in story
        return "minor"
    
    def _describe_deviation(self, emotion: str, expected: str, severity: str) -> str:
        """Generate human-readable deviation description."""
        if severity == "severe":
            return f"Severe deviation: {emotion} (expected {expected})"
        elif severity == "moderate":
            return f"Notable shift: {emotion} contradicts {expected} pattern"
        else:
            return f"Minor variation: {emotion} differs from {expected} baseline"
    
    def _calculate_consistency_score(self, emotions: List[str], deviations: List[Dict]) -> float:
        """Calculate 0-100 consistency score."""
        if not emotions:
            return 0.0
        
        # Base score starts at 100
        score = 100.0
        
        # Penalize for deviations
        for dev in deviations:
            if dev["severity"] == "severe":
                score -= 15
            elif dev["severity"] == "moderate":
                score -= 8
            else:
                score -= 3
        
        # Bonus for stable patterns (low emotion variety)
        unique_emotions = len(set(emotions))
        if unique_emotions <= 2:
            score += 10
        elif unique_emotions <= 3:
            score += 5
        
        return max(0.0, min(100.0, score))
    
    def _analyze_patterns(self, emotions: List[str], baseline: List[str]) -> str:
        """Analyze overall behavior pattern."""
        if not emotions:
            return "No data"
        
        unique_count = len(set(emotions))
        baseline_coverage = sum(1 for e in emotions if e in baseline) / len(emotions)
        
        if baseline_coverage > 0.8:
            return f"Highly consistent - {baseline_coverage:.0%} adherence to baseline {baseline}"
        elif baseline_coverage > 0.6:
            return f"Moderately consistent - {baseline_coverage:.0%} adherence with {unique_count} emotional states"
        elif baseline_coverage > 0.4:
            return f"Variable behavior - {baseline_coverage:.0%} baseline with significant variation"
        else:
            return f"Inconsistent - Only {baseline_coverage:.0%} baseline adherence, {unique_count} different emotions"
    
    def _generate_warnings(self, deviations: List[Dict], score: float, scene_count: int) -> List[str]:
        """Generate actionable warnings."""
        warnings = []
        
        # Severe deviations
        severe_devs = [d for d in deviations if d["severity"] == "severe"]
        if severe_devs:
            warnings.append(f"⚠️ {len(severe_devs)} severe out-of-character moment(s) detected")
            for dev in severe_devs[:2]:  # Show first 2
                warnings.append(f"  • Scene {dev['scene']}: {dev['description']}")
        
        # Low consistency score
        if score < 50:
            warnings.append("⚠️ Character behavior is highly inconsistent - review for narrative coherence")
        elif score < 70:
            warnings.append("ℹ️ Some behavioral inconsistencies detected - consider character motivation")
        
        # Too few scenes
        if scene_count < 5:
            warnings.append(f"ℹ️ Limited data ({scene_count} scenes) - analysis confidence is low")
        
        # No warnings = good
        if not warnings:
            warnings.append("✅ Character behavior is consistent and well-established")
        
        return warnings
