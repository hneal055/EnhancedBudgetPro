"""
Phase 13.2: Arc Comparator Engine
Side-by-side character development analysis and comparison
"""

from typing import Dict, List, Tuple
import math


class ArcComparator:
    """
    Compare character arcs side-by-side:
    - Emotion trajectory overlay
    - Volatility comparison
    - Turning point synchronization
    - Relationship dynamics
    - Development metrics
    """
    
    def compare_arcs(self, char1_name: str, char1_arc: Dict, 
                     char2_name: str, char2_arc: Dict) -> Dict:
        """
        Compare two character arcs with comprehensive metrics.
        
        Args:
            char1_name: First character name
            char1_arc: First character's arc data
            char2_name: Second character name
            char2_arc: Second character's arc data
        
        Returns:
            Comprehensive comparison dictionary
        """
        comparison = {
            "characters": [char1_name, char2_name],
            "basic_metrics": self._compare_basic_metrics(char1_arc, char2_arc),
            "trajectory_comparison": self._compare_trajectories(char1_arc, char2_arc),
            "interaction_analysis": self._analyze_interactions(
                char1_name, char1_arc, char2_name, char2_arc
            ),
            "development_rates": self._compare_development_rates(char1_arc, char2_arc),
            "synchronization": self._analyze_synchronization(char1_arc, char2_arc)
        }
        
        return comparison
    
    def _compare_basic_metrics(self, arc1: Dict, arc2: Dict) -> Dict:
        """Compare fundamental arc metrics"""
        return {
            "volatility": {
                "char1": arc1.get("emotional_volatility", 0),
                "char2": arc2.get("emotional_volatility", 0),
                "difference": abs(arc1.get("emotional_volatility", 0) - 
                                 arc2.get("emotional_volatility", 0)),
                "winner": "char1" if arc1.get("emotional_volatility", 0) > 
                         arc2.get("emotional_volatility", 0) else "char2"
            },
            "scenes": {
                "char1": arc1.get("total_scenes", 0),
                "char2": arc2.get("total_scenes", 0),
                "difference": abs(arc1.get("total_scenes", 0) - arc2.get("total_scenes", 0)),
                "winner": "char1" if arc1.get("total_scenes", 0) > 
                         arc2.get("total_scenes", 0) else "char2"
            },
            "dialogue_density": {
                "char1": arc1.get("scenes_with_dialogue", 0) / max(arc1.get("total_scenes", 1), 1),
                "char2": arc2.get("scenes_with_dialogue", 0) / max(arc2.get("total_scenes", 1), 1),
            },
            "emotional_range": {
                "char1": len(arc1.get("emotional_range", [])),
                "char2": len(arc2.get("emotional_range", [])),
                "char1_emotions": arc1.get("emotional_range", []),
                "char2_emotions": arc2.get("emotional_range", []),
                "shared_emotions": list(set(arc1.get("emotional_range", [])) & 
                                       set(arc2.get("emotional_range", [])))
            }
        }
    
    def _compare_trajectories(self, arc1: Dict, arc2: Dict) -> Dict:
        """Compare emotional trajectories over narrative time"""
        arc1_scenes = arc1.get("arc", [])
        arc2_scenes = arc2.get("arc", [])
        
        if not arc1_scenes or not arc2_scenes:
            return {"available": False}
        
        # Extract intensities and tensions
        arc1_intensities = [s.get("intensity", 0) for s in arc1_scenes]
        arc1_tensions = [s.get("tension", 0) for s in arc1_scenes]
        
        arc2_intensities = [s.get("intensity", 0) for s in arc2_scenes]
        arc2_tensions = [s.get("tension", 0) for s in arc2_scenes]
        
        # Calculate trajectory direction
        arc1_direction = self._calculate_direction(arc1_intensities)
        arc2_direction = self._calculate_direction(arc2_intensities)
        
        # Calculate correlation (if similar scene counts)
        correlation = self._calculate_correlation(arc1_intensities, arc2_intensities)
        
        return {
            "available": True,
            "arc1_direction": arc1_direction,
            "arc2_direction": arc2_direction,
            "parallel": arc1_direction == arc2_direction,
            "correlation": correlation,
            "arc1_peak_location": self._find_peak_location(arc1_intensities),
            "arc2_peak_location": self._find_peak_location(arc2_intensities),
            "synchronized_peaks": self._peaks_synchronized(arc1_intensities, arc2_intensities)
        }
    
    def _analyze_interactions(self, name1: str, arc1: Dict, 
                             name2: str, arc2: Dict) -> Dict:
        """Analyze character interactions and shared scenes"""
        arc1_scenes = arc1.get("arc", [])
        arc2_scenes = arc2.get("arc", [])
        
        # Find shared scene headings
        arc1_headings = set(s.get("heading", "") for s in arc1_scenes)
        arc2_headings = set(s.get("heading", "") for s in arc2_scenes)
        
        shared_headings = arc1_headings & arc2_headings
        
        # Calculate interaction metrics
        total_possible = len(arc1_headings | arc2_headings)
        interaction_rate = len(shared_headings) / total_possible if total_possible > 0 else 0
        
        # Analyze emotional alignment in shared scenes
        alignment_scores = []
        for heading in shared_headings:
            arc1_scene = next((s for s in arc1_scenes if s.get("heading") == heading), None)
            arc2_scene = next((s for s in arc2_scenes if s.get("heading") == heading), None)
            
            if arc1_scene and arc2_scene:
                # Compare emotions
                emotion_match = arc1_scene.get("dominant_emotion") == arc2_scene.get("dominant_emotion")
                intensity_diff = abs(arc1_scene.get("intensity", 0) - arc2_scene.get("intensity", 0))
                
                alignment_scores.append({
                    "scene": heading,
                    "emotion_match": emotion_match,
                    "intensity_diff": intensity_diff
                })
        
        avg_alignment = sum(1 for a in alignment_scores if a["emotion_match"]) / len(alignment_scores) if alignment_scores else 0
        
        return {
            "shared_scenes": len(shared_headings),
            "char1_only_scenes": len(arc1_headings - arc2_headings),
            "char2_only_scenes": len(arc2_headings - arc1_headings),
            "interaction_rate": interaction_rate,
            "emotional_alignment": avg_alignment,
            "alignment_details": alignment_scores[:10]  # Top 10 for display
        }
    
    def _compare_development_rates(self, arc1: Dict, arc2: Dict) -> Dict:
        """Compare how quickly characters develop emotionally"""
        arc1_scenes = arc1.get("arc", [])
        arc2_scenes = arc2.get("arc", [])
        
        if len(arc1_scenes) < 3 or len(arc2_scenes) < 3:
            return {"available": False}
        
        # Calculate development rate (change per scene)
        arc1_intensities = [s.get("intensity", 0) for s in arc1_scenes]
        arc2_intensities = [s.get("intensity", 0) for s in arc2_scenes]
        
        arc1_rate = abs(arc1_intensities[-1] - arc1_intensities[0]) / len(arc1_intensities)
        arc2_rate = abs(arc2_intensities[-1] - arc2_intensities[0]) / len(arc2_intensities)
        
        # Calculate arc depth (emotional range traversed)
        arc1_depth = max(arc1_intensities) - min(arc1_intensities)
        arc2_depth = max(arc2_intensities) - min(arc2_intensities)
        
        # Consistency score (lower volatility = more consistent)
        arc1_consistency = 100 - min(arc1.get("emotional_volatility", 0), 100)
        arc2_consistency = 100 - min(arc2.get("emotional_volatility", 0), 100)
        
        return {
            "available": True,
            "development_rate": {
                "char1": arc1_rate,
                "char2": arc2_rate,
                "faster": "char1" if arc1_rate > arc2_rate else "char2"
            },
            "arc_depth": {
                "char1": arc1_depth,
                "char2": arc2_depth,
                "deeper": "char1" if arc1_depth > arc2_depth else "char2"
            },
            "consistency": {
                "char1": arc1_consistency,
                "char2": arc2_consistency,
                "more_consistent": "char1" if arc1_consistency > arc2_consistency else "char2"
            }
        }
    
    def _analyze_synchronization(self, arc1: Dict, arc2: Dict) -> Dict:
        """Analyze whether character arcs are synchronized or complementary"""
        arc1_scenes = arc1.get("arc", [])
        arc2_scenes = arc2.get("arc", [])
        
        if not arc1_scenes or not arc2_scenes:
            return {"synchronized": False, "reason": "Insufficient data"}
        
        # Check if peaks occur at similar times
        arc1_intensities = [s.get("intensity", 0) for s in arc1_scenes]
        arc2_intensities = [s.get("intensity", 0) for s in arc2_scenes]
        
        peaks_synced = self._peaks_synchronized(arc1_intensities, arc2_intensities)
        
        # Check if emotional directions match
        arc1_direction = self._calculate_direction(arc1_intensities)
        arc2_direction = self._calculate_direction(arc2_intensities)
        
        parallel = arc1_direction == arc2_direction
        
        # Determine relationship type
        if peaks_synced and parallel:
            relationship = "Synchronized Allies"
            description = "Characters develop together with aligned emotional trajectories"
        elif peaks_synced and not parallel:
            relationship = "Synchronized Opposites"
            description = "Characters peak together but move in opposite emotional directions"
        elif not peaks_synced and parallel:
            relationship = "Asynchronous Allies"
            description = "Characters move in same emotional direction but at different paces"
        else:
            relationship = "Independent Arcs"
            description = "Characters develop independently with minimal synchronization"
        
        return {
            "synchronized": peaks_synced,
            "parallel": parallel,
            "relationship_type": relationship,
            "description": description
        }
    
    # Helper methods
    
    def _calculate_direction(self, values: List[float]) -> str:
        """Calculate overall trajectory direction"""
        if not values or len(values) < 2:
            return "flat"
        
        first_third = sum(values[:len(values)//3]) / max(len(values)//3, 1)
        last_third = sum(values[-len(values)//3:]) / max(len(values)//3, 1)
        
        delta = last_third - first_third
        
        if delta > 10:
            return "ascending"
        elif delta < -10:
            return "descending"
        else:
            return "flat"
    
    def _find_peak_location(self, values: List[float]) -> float:
        """Find peak location as percentage (0.0-1.0)"""
        if not values:
            return 0.5
        
        peak_idx = values.index(max(values))
        return peak_idx / len(values)
    
    def _peaks_synchronized(self, values1: List[float], values2: List[float]) -> bool:
        """Check if peaks occur at similar narrative positions"""
        peak1 = self._find_peak_location(values1)
        peak2 = self._find_peak_location(values2)
        
        # Within 20% of narrative = synchronized
        return abs(peak1 - peak2) < 0.2
    
    def _calculate_correlation(self, values1: List[float], values2: List[float]) -> float:
        """Calculate correlation between two value series"""
        # Normalize to same length by interpolation
        min_len = min(len(values1), len(values2))
        
        if min_len < 3:
            return 0.0
        
        # Simple correlation measure
        v1_normalized = self._normalize_series(values1, min_len)
        v2_normalized = self._normalize_series(values2, min_len)
        
        # Pearson-like correlation
        mean1 = sum(v1_normalized) / len(v1_normalized)
        mean2 = sum(v2_normalized) / len(v2_normalized)
        
        numerator = sum((v1_normalized[i] - mean1) * (v2_normalized[i] - mean2) 
                       for i in range(min_len))
        
        denom1 = math.sqrt(sum((v - mean1) ** 2 for v in v1_normalized))
        denom2 = math.sqrt(sum((v - mean2) ** 2 for v in v2_normalized))
        
        if denom1 == 0 or denom2 == 0:
            return 0.0
        
        correlation = numerator / (denom1 * denom2)
        return max(-1.0, min(1.0, correlation))  # Clamp to [-1, 1]
    
    def _normalize_series(self, values: List[float], target_length: int) -> List[float]:
        """Normalize series to target length via simple sampling"""
        if len(values) == target_length:
            return values
        
        if len(values) < target_length:
            # Upsample by repeating
            return values + [values[-1]] * (target_length - len(values))
        else:
            # Downsample by stride
            stride = len(values) / target_length
            return [values[int(i * stride)] for i in range(target_length)]
