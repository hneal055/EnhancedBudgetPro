"""
Scale Testing Visualization
Generate charts showing performance characteristics
"""

import matplotlib.pyplot as plt
import numpy as np

# Data from scale testing
scenes = [3, 10, 25, 50, 75, 100]
emotion_time = [1.37, 0.59, 1.31, 2.68, 4.15, 5.68]
throughput = [4.4, 133.7, 141.0, 144.0, 146.7, 145.1]
scene_analysis_time = [1.33, 0.35, 0.76, 1.65, 2.53, 3.43]
char_analysis_time = [0.04, 0.24, 0.54, 1.03, 1.62, 2.25]

# Create figure with 3 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('PILOTFORGEAI - Scale Performance Analysis', fontsize=16, fontweight='bold')

# 1. Total Analysis Time vs. Scenes
ax1 = axes[0, 0]
ax1.plot(scenes, emotion_time, 'o-', linewidth=2, markersize=8, color='#2E86AB', label='Actual')
# Add ideal linear scaling line (from 10-scene baseline)
ideal_baseline = 0.59 / 10
ideal_line = [s * ideal_baseline for s in scenes]
ax1.plot(scenes, ideal_line, '--', linewidth=2, color='#A23B72', label='Ideal Linear', alpha=0.7)
ax1.set_xlabel('Number of Scenes', fontsize=11)
ax1.set_ylabel('Analysis Time (seconds)', fontsize=11)
ax1.set_title('Analysis Time vs. Script Size', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# 2. Throughput vs. Scenes
ax2 = axes[0, 1]
ax2.plot(scenes[1:], throughput[1:], 's-', linewidth=2, markersize=8, color='#06A77D')
ax2.axhline(y=np.mean(throughput[1:]), color='#F18F01', linestyle='--', linewidth=2, label=f'Average: {np.mean(throughput[1:]):.1f} lines/sec')
ax2.set_xlabel('Number of Scenes', fontsize=11)
ax2.set_ylabel('Throughput (lines/sec)', fontsize=11)
ax2.set_title('Throughput Consistency (10-100 scenes)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.set_ylim([120, 160])

# 3. Time Breakdown (Stacked Bar)
ax3 = axes[1, 0]
width = 0.6
x_pos = np.arange(len(scenes))
ax3.bar(x_pos, scene_analysis_time, width, label='Scene Analysis', color='#4A90E2')
ax3.bar(x_pos, char_analysis_time, width, bottom=scene_analysis_time, label='Character Analysis', color='#E57373')
ax3.set_xlabel('Script Size', fontsize=11)
ax3.set_ylabel('Time (seconds)', fontsize=11)
ax3.set_title('Analysis Time Breakdown', fontsize=12, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels([f'{s}' for s in scenes])
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# 4. Scaling Efficiency
ax4 = axes[1, 1]
scene_ratios = [s / scenes[0] for s in scenes]
time_ratios = [t / emotion_time[0] for t in emotion_time]
efficiency = [sr / tr if tr > 0 else 0 for sr, tr in zip(scene_ratios, time_ratios)]

ax4.plot(scenes, efficiency, '^-', linewidth=2, markersize=8, color='#9B59B6')
ax4.axhline(y=1.0, color='#E74C3C', linestyle='--', linewidth=2, label='Ideal (1.0x)')
ax4.axhline(y=np.mean(efficiency[1:]), color='#27AE60', linestyle='--', linewidth=2, label=f'Average: {np.mean(efficiency[1:]):.2f}x', alpha=0.7)
ax4.set_xlabel('Number of Scenes', fontsize=11)
ax4.set_ylabel('Scaling Efficiency (x)', fontsize=11)
ax4.set_title('Scaling Efficiency Factor', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend()

plt.tight_layout()
plt.savefig('scale_performance_charts.png', dpi=150, bbox_inches='tight')
print("✅ Generated: scale_performance_charts.png")

# Create summary statistics
print("\n" + "="*60)
print("PERFORMANCE STATISTICS")
print("="*60)
print(f"Average Throughput (10-100 scenes): {np.mean(throughput[1:]):.1f} lines/sec")
print(f"Throughput Std Dev: {np.std(throughput[1:]):.1f} lines/sec ({np.std(throughput[1:])/np.mean(throughput[1:])*100:.1f}%)")
print(f"Average Scaling Efficiency (10-100): {np.mean(efficiency[1:]):.2f}x")
print(f"100-scene analysis time: {emotion_time[-1]:.2f}s")
print(f"Estimated feature film (120 scenes): {emotion_time[-1] * 1.2:.2f}s")
print("="*60 + "\n")
