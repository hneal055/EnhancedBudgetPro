"""
Scene-Character Index Optimization Test
Measures the impact of pre-built index vs. iteration
"""

import time
from src.IngestEngine.fdx_loader import load_fdx
from src.EmotionEngine import EmotionAnalyzer

def test_without_index(script_path):
    """Test character analysis WITHOUT scene-character index."""
    print("\n" + "="*60)
    print("WITHOUT SCENE-CHARACTER INDEX (Iteration)")
    print("="*60)
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    characters = parsed["characters"][:20]
    
    print(f"Scenes: {len(scenes)}, Characters: {len(characters)}")
    
    analyzer = EmotionAnalyzer()
    
    # Analyze without index (pass None)
    start = time.time()
    character_arcs = {}
    for char in characters:
        result = analyzer.analyze_character(char, scenes, scene_index=None)
        if result["scenes_with_dialogue"] > 0:
            character_arcs[char] = result
    elapsed = time.time() - start
    
    print(f"✅ Without index: {len(character_arcs)} characters in {elapsed:.2f}s")
    print(f"   Rate: {len(character_arcs)/elapsed:.1f} chars/sec")
    
    return elapsed, len(character_arcs)


def test_with_index(script_path):
    """Test character analysis WITH scene-character index."""
    print("\n" + "="*60)
    print("WITH SCENE-CHARACTER INDEX (Optimized)")
    print("="*60)
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    characters = parsed["characters"][:20]
    
    print(f"Scenes: {len(scenes)}, Characters: {len(characters)}")
    
    analyzer = EmotionAnalyzer()
    
    # Build index once
    index_start = time.time()
    scene_index = analyzer.build_scene_character_index(scenes)
    index_time = time.time() - index_start
    
    print(f"Index build time: {index_time:.3f}s ({len(scene_index)} characters)")
    
    # Analyze with index
    start = time.time()
    character_arcs = {}
    for char in characters:
        result = analyzer.analyze_character(char, scenes, scene_index=scene_index)
        if result["scenes_with_dialogue"] > 0:
            character_arcs[char] = result
    elapsed = time.time() - start
    
    total_time = index_time + elapsed
    
    print(f"✅ With index: {len(character_arcs)} characters in {elapsed:.2f}s (+ {index_time:.3f}s index)")
    print(f"   Total: {total_time:.2f}s")
    print(f"   Rate: {len(character_arcs)/total_time:.1f} chars/sec")
    
    return total_time, len(character_arcs), index_time


def test_parallel_with_index(script_path, workers=4):
    """Test parallel analysis WITH scene-character index (current implementation)."""
    print("\n" + "="*60)
    print(f"PARALLEL + INDEX (Phase 13.5, {workers} workers)")
    print("="*60)
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    characters = parsed["characters"][:20]
    
    print(f"Scenes: {len(scenes)}, Characters: {len(characters)}")
    
    analyzer = EmotionAnalyzer()
    
    # Parallel analysis (automatically builds and uses index)
    start = time.time()
    character_arcs = analyzer.analyze_characters_parallel(
        characters, 
        scenes,
        max_workers=workers
    )
    elapsed = time.time() - start
    
    print(f"✅ Parallel + index: {len(character_arcs)} characters in {elapsed:.2f}s")
    print(f"   Rate: {len(character_arcs)/elapsed:.1f} chars/sec")
    
    return elapsed, len(character_arcs)


if __name__ == "__main__":
    scripts = [
        ("samples/scale_tests/test_script_50scenes.fdx", "50-scene script"),
        ("samples/scale_tests/test_script_100scenes.fdx", "100-scene script")
    ]
    
    results = []
    
    for script_path, label in scripts:
        print(f"\n{'#'*60}")
        print(f"TESTING: {label}")
        print(f"{'#'*60}")
        
        # Test without index
        no_idx_time, no_idx_chars = test_without_index(script_path)
        
        # Test with index
        with_idx_time, with_idx_chars, index_build = test_with_index(script_path)
        
        # Test parallel with index
        parallel_time, parallel_chars = test_parallel_with_index(script_path, workers=4)
        
        # Calculate speedups
        index_speedup = no_idx_time / with_idx_time
        parallel_speedup = no_idx_time / parallel_time
        
        print(f"\n📊 COMPARISON:")
        print(f"   Index speedup: {index_speedup:.2f}x")
        print(f"   Parallel + Index speedup: {parallel_speedup:.2f}x")
        
        results.append({
            "script": label,
            "no_index": no_idx_time,
            "with_index": with_idx_time,
            "parallel_index": parallel_time,
            "index_speedup": index_speedup,
            "parallel_speedup": parallel_speedup
        })
    
    # Summary
    print("\n" + "="*60)
    print("OPTIMIZATION SUMMARY")
    print("="*60)
    print(f"{'Script':<20} {'No Index':>10} {'+ Index':>10} {'+ Parallel':>12} {'Total Gain':>12}")
    print("-"*60)
    
    for r in results:
        print(f"{r['script']:<20} {r['no_index']:>9.2f}s {r['with_index']:>9.2f}s {r['parallel_index']:>11.2f}s {r['parallel_speedup']:>11.2f}x")
    
    avg_index = sum(r['index_speedup'] for r in results) / len(results)
    avg_total = sum(r['parallel_speedup'] for r in results) / len(results)
    
    print("\n" + "="*60)
    print(f"Average Index Benefit: {avg_index:.2f}x")
    print(f"Average Total Benefit (Parallel + Index): {avg_total:.2f}x")
    print("="*60 + "\n")
