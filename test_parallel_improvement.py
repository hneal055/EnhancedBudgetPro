"""
Parallel Character Analysis - Before/After Comparison
Measures actual improvement from parallel processing
"""

import time
from src.IngestEngine.fdx_loader import load_fdx
from src.EmotionEngine import EmotionAnalyzer

def test_sequential(script_path):
    """Test sequential character analysis (old way)."""
    print("\n" + "="*60)
    print("SEQUENTIAL CHARACTER ANALYSIS (Old)")
    print("="*60)
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    characters = parsed["characters"][:20]
    
    print(f"Scenes: {len(scenes)}, Characters: {len(characters)}")
    
    analyzer = EmotionAnalyzer()
    
    # Sequential analysis
    start = time.time()
    character_arcs = {}
    for char in characters:
        result = analyzer.analyze_character(char, scenes)
        if result["scenes_with_dialogue"] > 0:
            character_arcs[char] = result
    elapsed = time.time() - start
    
    print(f"✅ Sequential: {len(character_arcs)} characters in {elapsed:.2f}s")
    print(f"   Rate: {len(character_arcs)/elapsed:.1f} chars/sec")
    
    return elapsed, len(character_arcs)


def test_parallel(script_path, max_workers=4):
    """Test parallel character analysis (new way)."""
    print("\n" + "="*60)
    print(f"PARALLEL CHARACTER ANALYSIS (New, {max_workers} workers)")
    print("="*60)
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    characters = parsed["characters"][:20]
    
    print(f"Scenes: {len(scenes)}, Characters: {len(characters)}")
    
    analyzer = EmotionAnalyzer()
    
    # Parallel analysis
    start = time.time()
    character_arcs = analyzer.analyze_characters_parallel(
        characters, 
        scenes,
        max_workers=max_workers
    )
    elapsed = time.time() - start
    
    print(f"✅ Parallel: {len(character_arcs)} characters in {elapsed:.2f}s")
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
        
        # Test sequential
        seq_time, seq_chars = test_sequential(script_path)
        
        # Test parallel with different worker counts
        for workers in [2, 4]:
            par_time, par_chars = test_parallel(script_path, max_workers=workers)
            speedup = seq_time / par_time
            
            print(f"\n🚀 Speedup ({workers} workers): {speedup:.2f}x faster")
            
            results.append({
                "script": label,
                "workers": workers,
                "sequential": seq_time,
                "parallel": par_time,
                "speedup": speedup,
                "chars": seq_chars
            })
    
    # Summary
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON SUMMARY")
    print("="*60)
    print(f"{'Script':<20} {'Workers':>8} {'Sequential':>12} {'Parallel':>10} {'Speedup':>10}")
    print("-"*60)
    
    for r in results:
        print(f"{r['script']:<20} {r['workers']:>8} {r['sequential']:>11.2f}s {r['parallel']:>9.2f}s {r['speedup']:>9.2f}x")
    
    avg_speedup = sum(r['speedup'] for r in results) / len(results)
    print("\n" + "="*60)
    print(f"Average Speedup: {avg_speedup:.2f}x")
    print("="*60 + "\n")
