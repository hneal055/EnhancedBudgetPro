# src/ScriptIngest.py

import os
import argparse

from src.IngestEngine.file_router import detect_format, route_file
from src.BudgetEngine import estimate_budget
from src.RiskModel import assess_risks
from src.ExportEngine import export_all
from src.errors import UnsupportedFormatError, ParseError
from src.validation import validate_parsed_script
from src.logging_cfg import get_logger

# Phase 13.1: Emotional Intelligence Integration
from src.EmotionEngine import EmotionAnalyzer, ArcTracker

# Phase 13.2: Advanced Character Arc Analysis
from src.CharacterArcEngine.arc_classifier import ArcClassifier
from src.CharacterArcEngine.arc_comparator import ArcComparator
from src.CharacterArcEngine.interaction_heatmap import InteractionHeatmap
from src.CharacterArcEngine.arc_predictor import ArcPredictor
from src.CharacterArcEngine.relationship_tracker import RelationshipTracker
from src.CharacterArcEngine.consistency_analyzer import ConsistencyAnalyzer
from src.CharacterArcEngine.storytelling_insights import StorytellingInsights
from src.CharacterArcEngine.character_analysis_exporter import CharacterAnalysisExporter

logger = get_logger()


def parse_script(path: str):
    fmt = detect_format(path)
    if fmt is None:
        raise UnsupportedFormatError(f"Unsupported format for file: {path}")
    data = route_file(path)
    try:
        validate_parsed_script(data)
    except Exception as e:
        raise ParseError(str(e))
    return data


def analyze_emotions(scenes: list, characters: list) -> dict:
    """
    Phase 13.1: Emotional Intelligence Analysis
    
    Analyzes emotional content across script:
    - Scene-level emotion detection
    - Character emotional arcs
    - Turning points and transformations
    
    Args:
        scenes: List of scene dicts from IngestEngine
        characters: List of character names
        
    Returns:
        Dict with {
            "scene_emotions": List[Dict],
            "character_arcs": Dict[str, Dict],
            "turning_points": Dict[str, List],
            "summary": Dict
        }
    """
    logger.info("🧠 Analyzing emotional intelligence...")
    
    try:
        analyzer = EmotionAnalyzer()
        tracker = ArcTracker()
        
        # Analyze each scene's emotional content
        scene_emotions = []
        for scene in scenes:
            scene_analysis = analyzer.analyze_scene(scene)
            scene_emotions.append(scene_analysis)
        
        # Analyze character emotional arcs in parallel (Phase 13.4)
        num_chars = min(len(characters), 20)
        # Optimal workers: min(CPU count, character count, 8)
        # More workers help with more characters
        optimal_workers = min(8, num_chars, 8)  # Max 8 workers
        
        logger.info(f"🚀 Analyzing {num_chars} characters in parallel ({optimal_workers} workers)...")
        
        # Use parallel analysis for 1.5-3x performance improvement
        character_arcs = analyzer.analyze_characters_parallel(
            characters[:20],  # Limit to top 20 to avoid excessive processing
            scenes,
            max_workers=optimal_workers
        )
        
        logger.info(f"✅ Character analysis complete: {len(character_arcs)} arcs tracked")
        
        # Identify turning points for each character
        turning_points = {}
        for char_name, char_arc in character_arcs.items():
            char_turning_points = tracker.identify_turning_points(char_arc)
            if char_turning_points:
                turning_points[char_name] = char_turning_points
        
        # Calculate summary statistics
        total_intensity = sum(s["intensity"] for s in scene_emotions)
        avg_intensity = total_intensity / len(scene_emotions) if scene_emotions else 0
        
        total_tension = sum(s["tension"] for s in scene_emotions)
        avg_tension = total_tension / len(scene_emotions) if scene_emotions else 0
        
        # Count dominant emotions across all scenes
        emotion_counts = {}
        for scene in scene_emotions:
            emotion = scene["dominant_emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        summary = {
            "total_scenes_analyzed": len(scene_emotions),
            "average_intensity": round(avg_intensity, 2),
            "average_tension": round(avg_tension, 2),
            "emotion_distribution": emotion_counts,
            "characters_with_arcs": len(character_arcs),
            "total_turning_points": sum(len(tp) for tp in turning_points.values())
        }
        
        logger.info(f"✅ Emotional analysis complete: {len(scene_emotions)} scenes, {len(character_arcs)} character arcs")
        
        return {
            "scene_emotions": scene_emotions,
            "character_arcs": character_arcs,
            "turning_points": turning_points,
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"❌ Emotional analysis failed: {e}")
        # Return empty structure if analysis fails (non-blocking)
        return {
            "scene_emotions": [],
            "character_arcs": {},
            "turning_points": {},
            "summary": {
                "total_scenes_analyzed": 0,
                "average_intensity": 0.0,
                "average_tension": 0.0,
                "emotion_distribution": {},
                "characters_with_arcs": 0,
                "total_turning_points": 0
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Film & TV Script Intelligence Engine")
    parser.add_argument("--input", required=True, help="Path to script file")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()

    script_path = args.input
    output_dir = args.out

    print(f"🔍 Reading: {script_path}")
    data = parse_script(script_path)
    
    # DEBUG: Check what parse_script returned
    if data.get("scenes") and len(data["scenes"]) > 0:
        first_scene = data["scenes"][0]
        logger.info(f"DEBUG run_full_analysis: First scene has {len(first_scene.get('lines', []))} lines")
        if first_scene.get('lines'):
            logger.info(f"DEBUG run_full_analysis: First line type: {type(first_scene['lines'][0])}")
            logger.info(f"DEBUG run_full_analysis: First line: {first_scene['lines'][0]}")

    scenes = data.get("scenes", [])
    characters = data.get("characters", [])

    print("\n================ RESULTS ================")
    print(f"📄 Scenes parsed:      {len(scenes)}")
    print(f"🎭 Characters found:   {len(set(characters))}")
    print("=========================================\n")

    # ---- Phase 2: Budget & Risk Engines ----
    budget_summary, budget_rows = estimate_budget(scenes)
    # Phase 13.1 Week 4: Pass emotion data to risk assessment
    emotion_data = analyze_emotions(scenes, characters)
    character_arcs = emotion_data.get("character_arcs", {})
    risk_rows = assess_risks(scenes, emotion_data)

    print("💰 Budget Summary:")
    print(
        f"   Total Budget:       ${budget_summary['total_budget']:.2f} {budget_summary['currency']}")
    print(
        f"   Avg/Scene:          ${budget_summary['average_cost_per_scene']:.2f}")
    print()

    print("⚠ Risk Overview:")
    high = sum(1 for r in risk_rows if r["risk_level"] == "HIGH")
    med = sum(1 for r in risk_rows if r["risk_level"] == "MEDIUM")
    low = sum(1 for r in risk_rows if r["risk_level"] == "LOW")
    print(f"   HIGH:   {high}")
    print(f"   MEDIUM: {med}")
    print(f"   LOW:    {low}")
    print()

    # ---- Phase 13.1: Emotional Intelligence (calculated above for risk) ----
    print("🧠 Emotional Intelligence:")
    print(f"   Scenes analyzed:    {emotion_data['summary']['total_scenes_analyzed']}")
    print(f"   Character arcs:     {emotion_data['summary']['characters_with_arcs']}")
    print(f"   Avg intensity:      {emotion_data['summary']['average_intensity']:.1f}/100")
    print(f"   Avg tension:        {emotion_data['summary']['average_tension']:.1f}/100")
    print()

    # ---- Export packet ----
    summary = export_all(
        scenes=scenes,
        characters=characters,
        budget_rows=budget_rows,
        risk_rows=risk_rows,
        output_dir=output_dir,
        script_path=script_path,
    )

    print("📦 Export complete:")
    print(f"   Output folder: {os.path.abspath(output_dir)}")
    print(f"   Summary JSON:  {os.path.join(output_dir, 'summary.json')}")
    print(
        f"   Excel report:  {os.path.join(output_dir, 'production_report.xlsx')}")
    print("\n✅ Done.")


def run_full_analysis(script_path: str, output_dir: str):
    """
    Core pipeline used by CLI / Web / tools:
      - parse script
      - compute budget
      - compute risk
      - analyze emotional intelligence (Phase 13.1)
      - export CSV / Excel / JSON
      - return all key structures
    """
    data = parse_script(script_path)
    
    # DEBUG: Check what parse_script returned
    if data.get("scenes") and len(data["scenes"]) > 0:
        first_scene = data["scenes"][0]
        logger.info(f"DEBUG run_full_analysis: First scene has {len(first_scene.get('lines', []))} lines")
        if first_scene.get('lines'):
            logger.info(f"DEBUG run_full_analysis: First line type: {type(first_scene['lines'][0])}")
            logger.info(f"DEBUG run_full_analysis: First line: {first_scene['lines'][0]}")

    scenes = data.get("scenes", [])
    characters = data.get("characters", [])

    budget_summary, budget_rows = estimate_budget(scenes)
    
    # Phase 13.1: Add emotional intelligence (calculate first for risk assessment)
    emotion_data = analyze_emotions(scenes, characters)
    character_arcs = emotion_data.get("character_arcs", {})
    
    # Phase 13.2: Advanced Character Arc Analysis
    arc_classifier = ArcClassifier()
    arc_comparator = ArcComparator()
    heatmap_generator = InteractionHeatmap()
    arc_predictor = ArcPredictor()
    relationship_tracker = RelationshipTracker()
    consistency_analyzer = ConsistencyAnalyzer()
    insights_generator = StorytellingInsights()
    
    # Run all Phase 13.2 analyses
    # Step 1: Classify arcs for all characters
    arc_classifications = arc_classifier.classify_all_characters(character_arcs)
    
    # Step 2: Predict completion for each character (needs arc_type from classification)
    arc_predictions = {}
    for char_name, char_arc in character_arcs.items():
        arc_type = arc_classifications.get(char_name, {}).get('arc_type', 'Unknown')
        arc_predictions[char_name] = arc_predictor.predict_completion(char_name, char_arc, arc_type)
    
    # Step 3: Track relationships (has batch method)
    relationship_evolution = relationship_tracker.track_all_relationships(character_arcs)
    
    # Step 4: Consistency analysis for each character
    consistency_analysis = {}
    for char_name, char_arc in character_arcs.items():
        consistency_analysis[char_name] = consistency_analyzer.analyze_consistency(char_name, char_arc)
    
    # Step 5: Character comparisons (skip for now - needs UI selection of char pairs)
    character_comparisons = []
    
    # Step 6: Interaction heatmap
    interaction_heatmap = heatmap_generator.generate_heatmap(character_arcs)
    
    # Step 7: Generate storytelling insights with all collected data
    storytelling_insights = insights_generator.generate_insights(
        character_arcs, 
        arc_classifications,
        character_comparisons,
        arc_predictions,
        relationship_evolution.get('relationships', []),  # Extract relationships list
        consistency_analysis
    )
    
    # Phase 13.1 Week 4: Pass emotion data to risk assessment
    risk_rows = assess_risks(scenes, emotion_data)

    export_summary = export_all(
        scenes=scenes,
        characters=characters,
        budget_rows=budget_rows,
        risk_rows=risk_rows,
        output_dir=output_dir,
        script_path=script_path,
    )

    return {
        "scenes": scenes,
        "characters": characters,
        "budget_summary": budget_summary,
        "budget_rows": budget_rows,
        "risk_rows": risk_rows,
        "emotion_data": emotion_data,  # NEW: Phase 13.1
        "export_summary": export_summary,
    }


if __name__ == "__main__":
    main()


def safe_run_full_analysis(script_path: str, output_dir: str):
    try:
        return run_full_analysis(script_path, output_dir)
    except Exception as e:
        logger.exception("run_full_analysis failed")
        return {"error": str(e)}
