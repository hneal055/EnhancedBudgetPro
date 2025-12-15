"""
Performance Profiling Script
Phase 13.3: Measure and compare analysis speeds

Tests emotion analysis performance with various script sizes.
"""

import time
from src.IngestEngine.fdx_loader import load_fdx
from src.EmotionEngine import EmotionAnalyzer
from src.logging_cfg import get_logger

logger = get_logger()


def profile_emotion_analysis(script_path: str):
    """Profile emotion analysis performance."""
    print(f"\n{'='*60}")
    print(f"PROFILING: {script_path}")
    print(f"{'='*60}\n")
    
    # Load script
    print("📄 Loading script...")
    load_start = time.time()
    parsed = load_fdx(script_path)
    load_time = time.time() - load_start
    
    scenes = parsed["scenes"]
    characters = parsed["characters"]
    
    print(f"✅ Loaded in {load_time:.2f}s")
    print(f"   - Scenes: {len(scenes)}")
    print(f"   - Characters: {len(characters)}")
    
    # Count dialogue lines
    total_lines = 0
    dialogue_lines = 0
    for scene in scenes:
        for line in scene.get("lines", []):
            if isinstance(line, dict):
                total_lines += 1
                if line.get("type") == "dialogue":
                    dialogue_lines += 1
    
    print(f"   - Total lines: {total_lines}")
    print(f"   - Dialogue lines: {dialogue_lines}")
    
    # Analyze emotions
    print("\n🧠 Analyzing emotions...")
    analyzer = EmotionAnalyzer()
    
    emotion_start = time.time()
    
    # Scene analysis
    scene_results = []
    for scene in scenes:
        result = analyzer.analyze_scene(scene)
        scene_results.append(result)
    
    scene_time = time.time() - emotion_start
    
    # Character analysis
    char_start = time.time()
    char_results = {}
    for char in characters[:20]:  # Limit to 20
        result = analyzer.analyze_character(char, scenes)
        if result["scenes_with_dialogue"] > 0:
            char_results[char] = result
    
    char_time = time.time() - char_start
    
    total_emotion_time = time.time() - emotion_start
    
    print(f"✅ Emotion analysis complete in {total_emotion_time:.2f}s")
    print(f"   - Scene analysis: {scene_time:.2f}s ({len(scenes)/scene_time:.1f} scenes/sec)")
    print(f"   - Character analysis: {char_time:.2f}s ({len(char_results)/char_time:.1f} chars/sec)")
    print(f"   - Character arcs tracked: {len(char_results)}")
    print(f"   - Throughput: {dialogue_lines/total_emotion_time:.1f} dialogue lines/sec")
    
    return {
        "load_time": load_time,
        "emotion_time": total_emotion_time,
        "scene_time": scene_time,
        "char_time": char_time,
        "scenes": len(scenes),
        "characters": len(char_results),
        "dialogue_lines": dialogue_lines,
        "total_lines": total_lines
    }


if __name__ == "__main__":
    # Profile test script
    results = profile_emotion_analysis("samples/test_script.fdx")
    
    print(f"\n{'='*60}")
    print("PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    print(f"Total Analysis Time: {results['emotion_time']:.2f}s")
    print(f"Throughput: {results['dialogue_lines']/results['emotion_time']:.1f} lines/sec")
    print(f"{'='*60}\n")
