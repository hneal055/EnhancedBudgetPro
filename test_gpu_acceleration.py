"""
GPU Acceleration Test
Tests EmotionDetector with CPU vs GPU (if available)
"""

import time
from src.EmotionEngine.detector import EmotionDetector
from src.IngestEngine.fdx_loader import load_fdx

def test_device_detection():
    """Test automatic device detection."""
    print("\n" + "="*60)
    print("GPU/CUDA DEVICE DETECTION")
    print("="*60)
    
    detector = EmotionDetector()  # Auto-detect
    device_info = detector.get_device_info()
    
    print(f"Device selected: {device_info['device']}")
    print(f"GPU enabled: {device_info['is_gpu']}")
    print(f"CUDA available: {device_info['cuda_available']}")
    
    if device_info['is_gpu']:
        print(f"GPU name: {device_info['gpu_name']}")
        print(f"GPU memory: {device_info['gpu_memory_gb']:.1f} GB")
        print(f"CUDA version: {device_info['pytorch_cuda_version']}")
        print("\n🚀 GPU acceleration ENABLED")
    else:
        print("\nℹ️  Running on CPU (no GPU detected)")
    
    return detector


def extract_text_lines(scenes):
    """Extract text from scene line dictionaries."""
    all_texts = []
    for scene in scenes:
        for line in scene["lines"]:
            if isinstance(line, dict) and "text" in line:
                all_texts.append(line["text"])
            elif isinstance(line, str):
                all_texts.append(line)
    return all_texts


def test_cpu_performance(script_path):
    """Test emotion detection on CPU."""
    print("\n" + "="*60)
    print("CPU PERFORMANCE BASELINE")
    print("="*60)
    
    # Force CPU
    detector = EmotionDetector(device='cpu')
    _ = detector.pipeline  # Pre-load model
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    
    # Extract all text lines
    all_texts = extract_text_lines(scenes)
    
    print(f"Scenes: {len(scenes)}, Lines: {len(all_texts)}")
    
    # Benchmark
    start = time.time()
    results = detector.detect_batch(all_texts)
    elapsed = time.time() - start
    
    throughput = len(all_texts) / elapsed
    print(f"✅ CPU: {len(all_texts)} lines in {elapsed:.2f}s")
    print(f"   Throughput: {throughput:.1f} lines/sec")
    
    return elapsed, throughput


def test_gpu_performance(script_path):
    """Test emotion detection on GPU (if available)."""
    print("\n" + "="*60)
    print("GPU PERFORMANCE TEST")
    print("="*60)
    
    # Try GPU
    detector = EmotionDetector(device='cuda')
    
    if not detector.is_gpu_enabled:
        print("❌ GPU not available, skipping GPU test")
        return None, None
    
    _ = detector.pipeline  # Pre-load model
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    
    # Extract all text lines
    all_texts = extract_text_lines(scenes)
    
    print(f"Scenes: {len(scenes)}, Lines: {len(all_texts)}")
    
    # Benchmark
    start = time.time()
    results = detector.detect_batch(all_texts)
    elapsed = time.time() - start
    
    throughput = len(all_texts) / elapsed
    print(f"✅ GPU: {len(all_texts)} lines in {elapsed:.2f}s")
    print(f"   Throughput: {throughput:.1f} lines/sec")
    
    return elapsed, throughput


def test_auto_detection_performance(script_path):
    """Test with auto-detection (production mode)."""
    print("\n" + "="*60)
    print("AUTO-DETECTION (Production Mode)")
    print("="*60)
    
    # Auto-detect (like production)
    detector = EmotionDetector()  # device=None = auto
    _ = detector.pipeline  # Pre-load model
    
    device_info = detector.get_device_info()
    print(f"Selected device: {device_info['device']}")
    
    parsed = load_fdx(script_path)
    scenes = parsed["scenes"]
    
    # Extract all text lines
    all_texts = extract_text_lines(scenes)
    
    print(f"Scenes: {len(scenes)}, Lines: {len(all_texts)}")
    
    # Benchmark
    start = time.time()
    results = detector.detect_batch(all_texts)
    elapsed = time.time() - start
    
    throughput = len(all_texts) / elapsed
    device_label = "GPU" if detector.is_gpu_enabled else "CPU"
    print(f"✅ Auto ({device_label}): {len(all_texts)} lines in {elapsed:.2f}s")
    print(f"   Throughput: {throughput:.1f} lines/sec")
    
    return elapsed, throughput


if __name__ == "__main__":
    scripts = [
        ("samples/scale_tests/test_script_50scenes.fdx", "50-scene script"),
        ("samples/scale_tests/test_script_100scenes.fdx", "100-scene script")
    ]
    
    # Device detection
    print("\n" + "#"*60)
    print("GPU ACCELERATION TEST SUITE")
    print("#"*60)
    detector = test_device_detection()
    
    for script_path, label in scripts:
        print(f"\n{'#'*60}")
        print(f"TESTING: {label}")
        print(f"{'#'*60}")
        
        # CPU baseline
        cpu_time, cpu_throughput = test_cpu_performance(script_path)
        
        # GPU test (if available)
        gpu_time, gpu_throughput = test_gpu_performance(script_path)
        
        # Auto-detection
        auto_time, auto_throughput = test_auto_detection_performance(script_path)
        
        # Summary
        print(f"\n📊 COMPARISON: {label}")
        print("-"*60)
        print(f"{'Mode':<15} {'Time':>10} {'Throughput':>15} {'Speedup':>10}")
        print("-"*60)
        print(f"{'CPU':<15} {cpu_time:>9.2f}s {cpu_throughput:>12.1f} l/s {'1.00x':>10}")
        
        if gpu_time and gpu_throughput:
            speedup = cpu_time / gpu_time
            print(f"{'GPU':<15} {gpu_time:>9.2f}s {gpu_throughput:>12.1f} l/s {speedup:>9.2f}x")
        
        auto_speedup = cpu_time / auto_time
        auto_label = "Auto (GPU)" if detector.is_gpu_enabled else "Auto (CPU)"
        print(f"{auto_label:<15} {auto_time:>9.2f}s {auto_throughput:>12.1f} l/s {auto_speedup:>9.2f}x")
        print("-"*60)
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    if detector.is_gpu_enabled:
        print("✅ GPU acceleration is working!")
    else:
        print("ℹ️  No GPU detected - code is GPU-ready")
        print("   When deployed with GPU, will auto-enable acceleration")
    print("="*60 + "\n")
