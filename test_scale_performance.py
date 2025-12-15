"""
Scale Performance Testing
Phase 13.3: Measure performance with large scripts

Tests emotion analysis performance at various scales:
- 3 scenes (original test)
- 10, 25, 50, 75, 100 scenes (generated)

Measures:
- Load time
- Emotion analysis time
- Scene analysis time
- Character analysis time
- Throughput (lines/sec)
- Memory usage (if available)
"""

import time
import os
from src.IngestEngine.fdx_loader import load_fdx
from src.EmotionEngine import EmotionAnalyzer
from src.logging_cfg import get_logger

logger = get_logger()


def profile_script(script_path: str, label: str):
    """Profile a single script and return metrics."""
    print(f"\n{'='*70}")
    print(f"TESTING: {label}")
    print(f"{'='*70}")
    print(f"File: {script_path}")
    
    # Check file size
    file_size = os.path.getsize(script_path) / 1024
    print(f"Size: {file_size:.1f} KB")
    
    # Load script
    print("\n📄 Loading script...")
    load_start = time.time()
    parsed = load_fdx(script_path)
    load_time = time.time() - load_start
    
    scenes = parsed["scenes"]
    characters = parsed["characters"]
    
    # Count lines
    total_lines = 0
    dialogue_lines = 0
    action_lines = 0
    for scene in scenes:
        for line in scene.get("lines", []):
            if isinstance(line, dict):
                total_lines += 1
                if line.get("type") == "dialogue":
                    dialogue_lines += 1
                elif line.get("type") == "action":
                    action_lines += 1
    
    print(f"✅ Loaded in {load_time:.2f}s")
    print(f"   Scenes: {len(scenes)}")
    print(f"   Characters: {len(characters)}")
    print(f"   Total lines: {total_lines}")
    print(f"   Dialogue lines: {dialogue_lines}")
    print(f"   Action lines: {action_lines}")
    
    # Analyze emotions
    print("\n🧠 Analyzing emotions...")
    analyzer = EmotionAnalyzer()
    
    emotion_start = time.time()
    
    # Scene analysis
    scene_start = time.time()
    scene_results = []
    for i, scene in enumerate(scenes):
        result = analyzer.analyze_scene(scene)
        scene_results.append(result)
        
        # Progress indicator for large scripts
        if (i + 1) % 25 == 0 or (i + 1) == len(scenes):
            elapsed = time.time() - scene_start
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            print(f"  Analyzed {i+1}/{len(scenes)} scenes ({rate:.1f} scenes/sec)...")
    
    scene_time = time.time() - scene_start
    
    # Character analysis
    char_start = time.time()
    char_results = {}
    for i, char in enumerate(characters[:20], 1):  # Limit to 20
        result = analyzer.analyze_character(char, scenes)
        if result["scenes_with_dialogue"] > 0:
            char_results[char] = result
        
        # Progress for character analysis
        if i % 5 == 0 or i == min(len(characters), 20):
            elapsed = time.time() - char_start
            rate = i / elapsed if elapsed > 0 else 0
            print(f"  Analyzed {i}/{min(len(characters), 20)} characters ({rate:.1f} chars/sec)...")
    
    char_time = time.time() - char_start
    
    total_emotion_time = time.time() - emotion_start
    
    print(f"\n✅ Emotion analysis complete in {total_emotion_time:.2f}s")
    print(f"   Scene analysis: {scene_time:.2f}s ({len(scenes)/scene_time:.1f} scenes/sec)")
    print(f"   Character analysis: {char_time:.2f}s ({len(char_results)/char_time if char_time > 0 else 0:.1f} chars/sec)")
    print(f"   Character arcs tracked: {len(char_results)}")
    
    # Calculate throughput
    total_throughput = total_lines / total_emotion_time if total_emotion_time > 0 else 0
    dialogue_throughput = dialogue_lines / total_emotion_time if total_emotion_time > 0 else 0
    
    print(f"   Throughput: {total_throughput:.1f} total lines/sec, {dialogue_throughput:.1f} dialogue lines/sec")
    
    return {
        "label": label,
        "file_size_kb": file_size,
        "load_time": load_time,
        "emotion_time": total_emotion_time,
        "scene_time": scene_time,
        "char_time": char_time,
        "total_time": load_time + total_emotion_time,
        "scenes": len(scenes),
        "characters": len(characters),
        "char_arcs": len(char_results),
        "total_lines": total_lines,
        "dialogue_lines": dialogue_lines,
        "action_lines": action_lines,
        "throughput_total": total_throughput,
        "throughput_dialogue": dialogue_throughput,
        "scenes_per_sec": len(scenes) / scene_time if scene_time > 0 else 0,
        "chars_per_sec": len(char_results) / char_time if char_time > 0 else 0
    }


def generate_report(results):
    """Generate comprehensive performance report."""
    print(f"\n{'='*70}")
    print("SCALE PERFORMANCE REPORT")
    print(f"{'='*70}\n")
    
    # Summary table
    print(f"{'Script':<20} {'Scenes':>7} {'Chars':>7} {'Lines':>8} {'Total':>9} {'Emotion':>9} {'Throughput':>12}")
    print(f"{'':<20} {'':<7} {'':<7} {'':<8} {'Time':>9} {'Time':>9} {'(lines/sec)':>12}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['label']:<20} {r['scenes']:>7} {r['char_arcs']:>7} {r['total_lines']:>8} "
              f"{r['total_time']:>8.2f}s {r['emotion_time']:>8.2f}s {r['throughput_total']:>12.1f}")
    
    print("\n" + "="*70)
    print("DETAILED ANALYSIS")
    print("="*70 + "\n")
    
    # Analyze scaling
    baseline = results[0]
    
    print("Scaling Analysis (vs. 3-scene baseline):")
    print(f"{'Script':<20} {'Scene':>7} {'Time':>9} {'Speedup':>9} {'Lines/sec':>12}")
    print(f"{'':20} {'Count':>7} {'Ratio':>9} {'Factor':>9} {'Change':>12}")
    print("-" * 70)
    
    for r in results:
        scene_ratio = r['scenes'] / baseline['scenes']
        time_ratio = r['emotion_time'] / baseline['emotion_time']
        speedup = scene_ratio / time_ratio if time_ratio > 0 else 0
        throughput_change = ((r['throughput_total'] - baseline['throughput_total']) / baseline['throughput_total'] * 100) if baseline['throughput_total'] > 0 else 0
        
        print(f"{r['label']:<20} {r['scenes']:>7} {time_ratio:>8.1f}x {speedup:>8.2f}x {throughput_change:>11.1f}%")
    
    print("\n" + "="*70)
    print("PERFORMANCE BREAKDOWN")
    print("="*70 + "\n")
    
    print(f"{'Script':<20} {'Load':>8} {'Scene':>9} {'Char':>9} {'Scene/s':>9} {'Char/s':>9}")
    print(f"{'':20} {'Time':>8} {'Analysis':>9} {'Analysis':>9} {'Rate':>9} {'Rate':>9}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['label']:<20} {r['load_time']:>7.2f}s {r['scene_time']:>8.2f}s {r['char_time']:>8.2f}s "
              f"{r['scenes_per_sec']:>8.1f} {r['chars_per_sec']:>8.1f}")
    
    print("\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70 + "\n")
    
    # Calculate average speedup
    speedups = []
    for r in results[1:]:  # Skip baseline
        scene_ratio = r['scenes'] / baseline['scenes']
        time_ratio = r['emotion_time'] / baseline['emotion_time']
        speedup = scene_ratio / time_ratio if time_ratio > 0 else 0
        speedups.append(speedup)
    
    avg_speedup = sum(speedups) / len(speedups) if speedups else 0
    
    # Find largest script
    largest = max(results, key=lambda x: x['scenes'])
    
    print(f"✅ Tested {len(results)} scripts ranging from {results[0]['scenes']} to {largest['scenes']} scenes")
    print(f"✅ Average scaling efficiency: {avg_speedup:.2f}x (ideal = 1.0x)")
    print(f"✅ Largest script ({largest['scenes']} scenes) analyzed in {largest['emotion_time']:.2f}s")
    print(f"✅ Throughput range: {min(r['throughput_total'] for r in results):.1f} - {max(r['throughput_total'] for r in results):.1f} lines/sec")
    
    # Performance rating
    if avg_speedup >= 0.9:
        rating = "🟢 EXCELLENT - Linear scaling maintained"
    elif avg_speedup >= 0.7:
        rating = "🟡 GOOD - Minor scaling degradation"
    elif avg_speedup >= 0.5:
        rating = "🟠 FAIR - Noticeable scaling issues"
    else:
        rating = "🔴 POOR - Significant scaling problems"
    
    print(f"\nPerformance Rating: {rating}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    # Test scripts
    test_scripts = [
        ("samples/test_script.fdx", "Original (3 scenes)"),
        ("samples/scale_tests/test_script_10scenes.fdx", "Small (10 scenes)"),
        ("samples/scale_tests/test_script_25scenes.fdx", "Medium (25 scenes)"),
        ("samples/scale_tests/test_script_50scenes.fdx", "Large (50 scenes)"),
        ("samples/scale_tests/test_script_75scenes.fdx", "XLarge (75 scenes)"),
        ("samples/scale_tests/test_script_100scenes.fdx", "XXLarge (100 scenes)")
    ]
    
    results = []
    
    for script_path, label in test_scripts:
        if os.path.exists(script_path):
            result = profile_script(script_path, label)
            results.append(result)
        else:
            print(f"\n⚠️  Skipping {label} - file not found: {script_path}")
    
    # Generate comprehensive report
    if results:
        generate_report(results)
