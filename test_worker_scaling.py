"""
Test parallel character analysis with different worker counts
"""

import time
from src.IngestEngine.fdx_loader import load_fdx
from src.EmotionEngine import EmotionAnalyzer

script_path = "samples/scale_tests/test_script_100scenes.fdx"

parsed = load_fdx(script_path)
scenes = parsed["scenes"]
characters = parsed["characters"][:20]

print(f"Testing: {len(scenes)} scenes, {len(characters)} characters\n")
print(f"{'Workers':<10} {'Time':>10} {'Rate':>12} {'Speedup':>10}")
print("-" * 45)

baseline_time = None

for workers in [1, 2, 3, 4, 6, 8]:
    analyzer = EmotionAnalyzer()
    
    start = time.time()
    character_arcs = analyzer.analyze_characters_parallel(
        characters,
        scenes,
        max_workers=workers
    )
    elapsed = time.time() - start
    
    rate = len(character_arcs) / elapsed
    
    if baseline_time is None:
        baseline_time = elapsed
        speedup_str = "baseline"
    else:
        speedup = baseline_time / elapsed
        speedup_str = f"{speedup:.2f}x"
    
    print(f"{workers:<10} {elapsed:>9.2f}s {rate:>10.1f}/s {speedup_str:>10}")

print()
