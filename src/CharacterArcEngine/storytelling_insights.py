"""
Storytelling Insights Dashboard
"AI Producer" recommendations aggregating all character analysis engines
"""
from typing import Dict, List, Any


class StorytellingInsights:
    """
    Aggregates data from all character analysis engines to provide
    holistic script health scores and actionable recommendations
    """
    
    def generate_insights(
        self,
        character_arcs: Dict[str, Dict],
        classifications: Dict[str, Dict],
        comparisons: List[Dict] = None,
        predictions: Dict[str, Dict] = None,
        relationships: List[Dict] = None,
        consistency: Dict[str, Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive storytelling insights
        
        Args:
            character_arcs: Raw emotion data per character
            classifications: Arc type classifications
            comparisons: Character comparison data (optional)
            predictions: Arc completion predictions (optional)
            relationships: Relationship evolution data (optional)
            consistency: Consistency analysis data (optional)
        
        Returns:
            Dict with overall_health, recommendations, pacing_analysis,
            arc_optimization, benchmarks, export_summary
        """
        
        # Calculate overall script health
        health_score = self._calculate_overall_health(
            character_arcs, classifications, predictions, consistency
        )
        
        # Generate character development recommendations
        recommendations = self._generate_recommendations(
            character_arcs, classifications, predictions, relationships, consistency
        )
        
        # Analyze pacing
        pacing_analysis = self._analyze_pacing(
            character_arcs, classifications, predictions
        )
        
        # Emotional arc optimization
        arc_optimization = self._optimize_emotional_arcs(
            character_arcs, classifications, predictions
        )
        
        # Benchmark against successful patterns
        benchmarks = self._benchmark_against_patterns(
            character_arcs, classifications
        )
        
        # Export-friendly summary
        export_summary = self._generate_export_summary(
            health_score, recommendations, pacing_analysis, arc_optimization
        )
        
        return {
            "overall_health": health_score,
            "recommendations": recommendations,
            "pacing_analysis": pacing_analysis,
            "arc_optimization": arc_optimization,
            "benchmarks": benchmarks,
            "export_summary": export_summary,
            "character_count": len(character_arcs),
            "analyzed_arcs": len([c for c in character_arcs if len(character_arcs[c].get("scenes", [])) >= 3])
        }
    
    def _calculate_overall_health(
        self,
        character_arcs: Dict,
        classifications: Dict,
        predictions: Dict,
        consistency: Dict
    ) -> Dict[str, Any]:
        """Calculate overall script health score (0-100)"""
        
        scores = []
        breakdown = {}
        
        # 1. Character Coverage (0-100)
        # Higher is better - more characters with meaningful arcs
        total_chars = len(character_arcs)
        analyzed_chars = len([c for c in character_arcs if len(character_arcs[c].get("scenes", [])) >= 3])
        coverage_score = (analyzed_chars / total_chars * 100) if total_chars > 0 else 0
        scores.append(coverage_score)
        breakdown["character_coverage"] = {
            "score": coverage_score,
            "analyzed": analyzed_chars,
            "total": total_chars
        }
        
        # 2. Arc Diversity (0-100)
        # Higher is better - variety of arc types
        if classifications:
            arc_types = set([c.get("arc_type", "Unknown") for c in classifications.values()])
            diversity_score = min(len(arc_types) * 20, 100)  # Max 5 unique types = 100
            scores.append(diversity_score)
            breakdown["arc_diversity"] = {
                "score": diversity_score,
                "unique_types": len(arc_types),
                "types": list(arc_types)
            }
        
        # 3. Arc Completion (0-100)
        # Higher is better - arcs closer to completion
        if predictions:
            completion_scores = [p["completion_percentage"] for p in predictions.values()]
            avg_completion = sum(completion_scores) / len(completion_scores) if completion_scores else 0
            scores.append(avg_completion)
            breakdown["arc_completion"] = {
                "score": avg_completion,
                "average": avg_completion,
                "range": f"{min(completion_scores):.0f}%-{max(completion_scores):.0f}%" if completion_scores else "N/A"
            }
        
        # 4. Consistency (0-100)
        # Higher is better - characters stay in character
        if consistency:
            consistency_scores = [c["consistency_score"] for c in consistency.values()]
            avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 80
            scores.append(avg_consistency)
            breakdown["consistency"] = {
                "score": avg_consistency,
                "average": avg_consistency,
                "issues": sum([len(c["deviations"]) for c in consistency.values()])
            }
        
        # Overall health = weighted average
        overall = sum(scores) / len(scores) if scores else 0
        
        # Rating
        if overall >= 85:
            rating = "Excellent"
            emoji = "🌟"
        elif overall >= 70:
            rating = "Good"
            emoji = "✅"
        elif overall >= 50:
            rating = "Fair"
            emoji = "⚠️"
        else:
            rating = "Needs Improvement"
            emoji = "🚨"
        
        return {
            "score": overall,
            "rating": rating,
            "emoji": emoji,
            "breakdown": breakdown,
            "strengths": self._identify_strengths(breakdown),
            "weaknesses": self._identify_weaknesses(breakdown)
        }
    
    def _identify_strengths(self, breakdown: Dict) -> List[str]:
        """Identify script's storytelling strengths"""
        strengths = []
        
        if breakdown.get("character_coverage", {}).get("score", 0) >= 80:
            strengths.append("Strong character coverage - most characters have developed arcs")
        
        if breakdown.get("arc_diversity", {}).get("score", 0) >= 60:
            strengths.append("Diverse arc types - variety keeps audience engaged")
        
        if breakdown.get("arc_completion", {}).get("score", 0) >= 70:
            strengths.append("Well-paced arcs - characters approaching satisfying resolutions")
        
        if breakdown.get("consistency", {}).get("score", 0) >= 80:
            strengths.append("Consistent characterization - believable behavior patterns")
        
        return strengths if strengths else ["Baseline storytelling structure established"]
    
    def _identify_weaknesses(self, breakdown: Dict) -> List[str]:
        """Identify areas needing improvement"""
        weaknesses = []
        
        if breakdown.get("character_coverage", {}).get("score", 0) < 50:
            weaknesses.append("Low character coverage - many characters lack meaningful arcs")
        
        if breakdown.get("arc_diversity", {}).get("score", 0) < 40:
            weaknesses.append("Limited arc variety - consider diversifying character journeys")
        
        if breakdown.get("arc_completion", {}).get("score", 0) < 50:
            weaknesses.append("Incomplete arcs - most characters need more development")
        
        if breakdown.get("consistency", {}).get("issues", 0) > 5:
            weaknesses.append("Multiple consistency issues - review out-of-character moments")
        
        return weaknesses if weaknesses else ["No critical issues detected"]
    
    def _generate_recommendations(
        self,
        character_arcs: Dict,
        classifications: Dict,
        predictions: Dict,
        relationships: List,
        consistency: Dict
    ) -> List[Dict[str, str]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Priority 1: Incomplete arcs
        if predictions:
            incomplete = [
                (char, p) for char, p in predictions.items()
                if p["completion_percentage"] < 60
            ]
            for char, pred in incomplete[:3]:  # Top 3
                recommendations.append({
                    "priority": "HIGH",
                    "category": "Arc Completion",
                    "character": char,
                    "issue": f"Arc only {pred['completion_percentage']:.0f}% complete",
                    "suggestion": f"Add scenes covering: {', '.join(pred['missing_beats'][:2])}"
                })
        
        # Priority 2: Consistency issues
        if consistency:
            severe_issues = [
                (char, c) for char, c in consistency.items()
                if any(d["severity"] == "severe" for d in c["deviations"])
            ]
            for char, cons in severe_issues[:2]:  # Top 2
                severe_devs = [d for d in cons["deviations"] if d["severity"] == "severe"]
                recommendations.append({
                    "priority": "HIGH",
                    "category": "Consistency",
                    "character": char,
                    "issue": f"{len(severe_devs)} severe out-of-character moment(s)",
                    "suggestion": f"Review scene {severe_devs[0]['scene']}: {severe_devs[0]['description']}"
                })
        
        # Priority 3: Weak relationships
        if relationships:
            weak_rels = [r for r in relationships if r.get("relationship_strength", 0) < 0.3]
            for rel in weak_rels[:2]:  # Top 2
                char1, char2 = rel["characters"]
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "Relationships",
                    "character": f"{char1} & {char2}",
                    "issue": f"Weak relationship ({rel['relationship_strength']:.0%})",
                    "suggestion": "Add scenes showing meaningful interaction or conflict"
                })
        
        # Priority 4: Arc diversity
        if classifications:
            arc_types = [c.get("arc_type") for c in classifications.values()]
            if len(set(arc_types)) < 3 and len(arc_types) >= 3:
                recommendations.append({
                    "priority": "LOW",
                    "category": "Diversity",
                    "character": "Overall",
                    "issue": f"Limited arc variety ({len(set(arc_types))} unique types)",
                    "suggestion": "Consider diversifying secondary character arcs"
                })
        
        # General recommendation if none triggered
        if not recommendations:
            recommendations.append({
                "priority": "LOW",
                "category": "General",
                "character": "Overall",
                "issue": "Script structure is solid",
                "suggestion": "Continue developing character emotional journeys"
            })
        
        return recommendations
    
    def _analyze_pacing(
        self,
        character_arcs: Dict,
        classifications: Dict,
        predictions: Dict
    ) -> Dict[str, Any]:
        """Analyze overall script pacing"""
        
        # Calculate average scene distribution
        scene_counts = [len(arc.get("scenes", [])) for arc in character_arcs.values()]
        avg_scenes = sum(scene_counts) / len(scene_counts) if scene_counts else 0
        
        # Identify pacing issues
        pacing_issues = []
        if predictions:
            for char, pred in predictions.items():
                if pred.get("pacing") == "Too Fast":
                    pacing_issues.append(f"{char}: Rushed development - spread arc across more scenes")
                elif pred.get("pacing") == "Too Slow":
                    pacing_issues.append(f"{char}: Stagnant arc - increase emotional progression rate")
        
        # Overall pacing assessment
        if avg_scenes < 3:
            overall = "Underdeveloped - Most characters need more scenes"
            emoji = "🐌"
        elif avg_scenes > 10:
            overall = "Complex - Many character interactions to track"
            emoji = "🏃"
        else:
            overall = "Balanced - Good scene distribution across characters"
            emoji = "⚖️"
        
        return {
            "average_scenes_per_character": avg_scenes,
            "overall_assessment": overall,
            "emoji": emoji,
            "pacing_issues": pacing_issues,
            "scene_distribution": {
                "min": min(scene_counts) if scene_counts else 0,
                "max": max(scene_counts) if scene_counts else 0,
                "avg": avg_scenes
            }
        }
    
    def _optimize_emotional_arcs(
        self,
        character_arcs: Dict,
        classifications: Dict,
        predictions: Dict
    ) -> List[Dict[str, Any]]:
        """Suggest emotional arc optimizations"""
        optimizations = []
        
        if not predictions:
            return optimizations
        
        for char, pred in predictions.items():
            opt = {
                "character": char,
                "current_completion": pred["completion_percentage"],
                "suggestions": []
            }
            
            # Missing emotional beats
            if pred["missing_beats"]:
                opt["suggestions"].append({
                    "type": "Add Beats",
                    "description": f"Include scenes with: {', '.join(pred['missing_beats'][:3])}",
                    "impact": "HIGH"
                })
            
            # Pacing adjustments
            if pred.get("pacing") == "Too Fast":
                opt["suggestions"].append({
                    "type": "Slow Down",
                    "description": "Add transitional scenes to show gradual emotional change",
                    "impact": "MEDIUM"
                })
            elif pred.get("pacing") == "Too Slow":
                opt["suggestions"].append({
                    "type": "Accelerate",
                    "description": "Remove redundant scenes or increase emotional stakes",
                    "impact": "MEDIUM"
                })
            
            # Transformation completion
            if pred.get("transformation_status") == "Incomplete":
                opt["suggestions"].append({
                    "type": "Complete Arc",
                    "description": "Add resolution scenes showing final character state",
                    "impact": "HIGH"
                })
            
            if opt["suggestions"]:
                optimizations.append(opt)
        
        return optimizations
    
    def _benchmark_against_patterns(
        self,
        character_arcs: Dict,
        classifications: Dict
    ) -> Dict[str, Any]:
        """Compare against successful screenplay patterns"""
        
        # Industry benchmarks (approximate)
        BENCHMARKS = {
            "protagonist_scenes": {"min": 15, "ideal": 25, "max": 40},
            "arc_types": {"min": 2, "ideal": 4, "max": 6},
            "emotional_range": {"min": 3, "ideal": 5, "max": 7},
            "consistency_score": {"min": 70, "ideal": 85, "max": 95}
        }
        
        # Calculate current metrics
        if character_arcs:
            max_scenes = max([len(arc.get("scenes", [])) for arc in character_arcs.values()])
            unique_arcs = len(set([c.get("arc_type", "Unknown") for c in classifications.values()])) if classifications else 0
            
            # Emotional range (unique emotions across all characters)
            all_emotions = set()
            for arc in character_arcs.values():
                for scene_data in arc.get("emotions_by_scene", {}).values():
                    all_emotions.add(scene_data.get("emotion", "neutral"))
            emotional_range = len(all_emotions)
        else:
            max_scenes = 0
            unique_arcs = 0
            emotional_range = 0
        
        # Compare to benchmarks
        comparisons = []
        
        # Protagonist scenes
        if max_scenes < BENCHMARKS["protagonist_scenes"]["min"]:
            comparisons.append({
                "metric": "Protagonist Screen Time",
                "status": "Below Industry Standard",
                "current": max_scenes,
                "benchmark": BENCHMARKS["protagonist_scenes"]["ideal"],
                "recommendation": "Increase protagonist scenes to establish stronger presence"
            })
        elif max_scenes > BENCHMARKS["protagonist_scenes"]["max"]:
            comparisons.append({
                "metric": "Protagonist Screen Time",
                "status": "Above Industry Standard",
                "current": max_scenes,
                "benchmark": BENCHMARKS["protagonist_scenes"]["ideal"],
                "recommendation": "Consider balancing with secondary character development"
            })
        else:
            comparisons.append({
                "metric": "Protagonist Screen Time",
                "status": "Meets Industry Standard",
                "current": max_scenes,
                "benchmark": BENCHMARKS["protagonist_scenes"]["ideal"],
                "recommendation": "Maintain current protagonist presence"
            })
        
        # Arc diversity
        if unique_arcs < BENCHMARKS["arc_types"]["min"]:
            comparisons.append({
                "metric": "Arc Diversity",
                "status": "Below Industry Standard",
                "current": unique_arcs,
                "benchmark": BENCHMARKS["arc_types"]["ideal"],
                "recommendation": "Add variety with different character arc types"
            })
        else:
            comparisons.append({
                "metric": "Arc Diversity",
                "status": "Meets Industry Standard",
                "current": unique_arcs,
                "benchmark": BENCHMARKS["arc_types"]["ideal"],
                "recommendation": "Good variety in character journeys"
            })
        
        # Emotional range
        if emotional_range < BENCHMARKS["emotional_range"]["min"]:
            comparisons.append({
                "metric": "Emotional Range",
                "status": "Limited",
                "current": emotional_range,
                "benchmark": BENCHMARKS["emotional_range"]["ideal"],
                "recommendation": "Expand emotional palette for richer storytelling"
            })
        else:
            comparisons.append({
                "metric": "Emotional Range",
                "status": "Strong",
                "current": emotional_range,
                "benchmark": BENCHMARKS["emotional_range"]["ideal"],
                "recommendation": "Excellent emotional variety"
            })
        
        return {
            "comparisons": comparisons,
            "overall_alignment": self._calculate_alignment_score(comparisons),
            "industry_note": "Benchmarks based on successful feature film patterns"
        }
    
    def _calculate_alignment_score(self, comparisons: List[Dict]) -> Dict[str, Any]:
        """Calculate how well script aligns with industry patterns"""
        meets_standard = sum([1 for c in comparisons if "Meets" in c["status"] or "Strong" in c["status"]])
        total = len(comparisons)
        alignment = (meets_standard / total * 100) if total > 0 else 0
        
        if alignment >= 75:
            return {"score": alignment, "rating": "Excellent Alignment", "emoji": "🎯"}
        elif alignment >= 50:
            return {"score": alignment, "rating": "Good Alignment", "emoji": "✅"}
        else:
            return {"score": alignment, "rating": "Needs Adjustment", "emoji": "⚠️"}
    
    def _generate_export_summary(
        self,
        health_score: Dict,
        recommendations: List,
        pacing: Dict,
        optimization: List
    ) -> Dict[str, Any]:
        """Generate export-friendly summary for reports"""
        
        return {
            "executive_summary": {
                "overall_health": f"{health_score['score']:.0f}/100 ({health_score['rating']})",
                "key_strengths": health_score["strengths"][:3],
                "key_weaknesses": health_score["weaknesses"][:3],
                "priority_actions": len([r for r in recommendations if r["priority"] == "HIGH"])
            },
            "quick_stats": {
                "characters_analyzed": health_score["breakdown"].get("character_coverage", {}).get("analyzed", 0),
                "arc_completion_avg": health_score["breakdown"].get("arc_completion", {}).get("average", 0),
                "consistency_avg": health_score["breakdown"].get("consistency", {}).get("average", 0),
                "pacing_status": pacing["overall_assessment"]
            },
            "top_priorities": [
                {
                    "character": r["character"],
                    "issue": r["issue"],
                    "action": r["suggestion"]
                }
                for r in recommendations[:5]
            ],
            "generated_at": "Phase 13.2 Week 2 Storytelling Insights Dashboard"
        }
