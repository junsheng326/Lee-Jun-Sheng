"""
CockroachDB Performance Visualization
YOUR ACTUAL TEST RESULTS - Ready to run!
"""

import matplotlib.pyplot as plt
import numpy as np

# ==============================================================================
# YOUR TEST RESULTS (Already filled in!)
# ==============================================================================

# LATENCY TEST RESULTS (in milliseconds)
latency_results = {
    '10K': 22.92,
    '100K': 7.03,
    '500K': 8.56
}

# SCALABILITY TEST RESULTS (in seconds)
scalability_results = {
    'small_dataset': {
        'documents': 30000,
        'read_time': 0.0043,
        'write_time': 0.0968,
        'query_time': 0.0023
    },
    'medium_dataset': {
        'documents': 200000,
        'read_time': 0.0026,
        'write_time': 0.0821,
        'query_time': 0.0082
    },
    'large_dataset': {
        'documents': 510370,
        'read_time': 0.0020,
        'write_time': 0.0349,
        'query_time': 0.0025
    }
}

# ==============================================================================
# VISUALIZATION CODE
# ==============================================================================

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('CockroachDB Performance Test Results', fontsize=18, fontweight='bold')

# Colors
color_latency = '#6933FF'  # CockroachDB purple
color_read = '#4CAF50'     # Green
color_write = '#FF9800'    # Orange
color_query = '#2196F3'    # Blue

# Dataset labels
dataset_labels = ['Small\n(30K)', 'Medium\n(200K)', 'Large\n(510K)']
dataset_sizes = [30000, 200000, 510370]

# ==============================================================================
# PLOT 1: Latency by Dataset Size (Bar Chart)
# ==============================================================================
ax1 = axes[0, 0]

latency_values = list(latency_results.values())
x = np.arange(len(dataset_labels))

bars = ax1.bar(x, latency_values, color=color_latency, alpha=0.7, edgecolor='black', linewidth=1.5)

ax1.set_xlabel('Dataset Size', fontsize=12, fontweight='bold')
ax1.set_ylabel('Latency (milliseconds)', fontsize=12, fontweight='bold')
ax1.set_title('Update Latency by Dataset Size', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(dataset_labels)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f} ms',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# ==============================================================================
# PLOT 2: Read Performance (Line Chart)
# ==============================================================================
ax2 = axes[0, 1]

read_times = [
    scalability_results['small_dataset']['read_time'],
    scalability_results['medium_dataset']['read_time'],
    scalability_results['large_dataset']['read_time']
]

ax2.plot(dataset_sizes, read_times, marker='o', linewidth=3, markersize=10, 
         color=color_read, label='Read 100 docs')
ax2.fill_between(dataset_sizes, read_times, alpha=0.3, color=color_read)

ax2.set_xlabel('Number of Documents', fontsize=12, fontweight='bold')
ax2.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
ax2.set_title('Read Performance\n(Fetching 100 documents)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')

# Add value labels on points
for i, (size, time) in enumerate(zip(dataset_sizes, read_times)):
    ax2.annotate(f'{time:.4f}s', 
                xy=(size, time), 
                xytext=(10, 10), 
                textcoords='offset points',
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7))

# ==============================================================================
# PLOT 3: Write Performance (Line Chart)
# ==============================================================================
ax3 = axes[1, 0]

write_times = [
    scalability_results['small_dataset']['write_time'],
    scalability_results['medium_dataset']['write_time'],
    scalability_results['large_dataset']['write_time']
]

ax3.plot(dataset_sizes, write_times, marker='s', linewidth=3, markersize=10, 
         color=color_write, label='Write 10 docs')
ax3.fill_between(dataset_sizes, write_times, alpha=0.3, color=color_write)

ax3.set_xlabel('Number of Documents', fontsize=12, fontweight='bold')
ax3.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
ax3.set_title('Write Performance\n(Inserting 10 documents)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, linestyle='--')

# Add value labels
for i, (size, time) in enumerate(zip(dataset_sizes, write_times)):
    ax3.annotate(f'{time:.4f}s', 
                xy=(size, time), 
                xytext=(10, -15), 
                textcoords='offset points',
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7))

# ==============================================================================
# PLOT 4: Query Performance (Line Chart)
# ==============================================================================
ax4 = axes[1, 1]

query_times = [
    scalability_results['small_dataset']['query_time'],
    scalability_results['medium_dataset']['query_time'],
    scalability_results['large_dataset']['query_time']
]

ax4.plot(dataset_sizes, query_times, marker='^', linewidth=3, markersize=10, 
         color=color_query, label='Query 50 docs')
ax4.fill_between(dataset_sizes, query_times, alpha=0.3, color=color_query)

ax4.set_xlabel('Number of Documents', fontsize=12, fontweight='bold')
ax4.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
ax4.set_title('Query Performance\n(Conditional query)', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, linestyle='--')

# Add value labels
for i, (size, time) in enumerate(zip(dataset_sizes, query_times)):
    ax4.annotate(f'{time:.4f}s', 
                xy=(size, time), 
                xytext=(10, 10), 
                textcoords='offset points',
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7))

# ==============================================================================
# SAVE AND SHOW
# ==============================================================================
plt.tight_layout()
plt.savefig('cockroach_performance_results.png', dpi=300, bbox_inches='tight')

print("=" * 60)
print("✓ Visualization saved as 'cockroach_performance_results.png'")
print("=" * 60)
print("\nPerformance Summary:")
print(f"  Latency (30K):    {latency_results['10K']:.2f} ms")
print(f"  Latency (200K):   {latency_results['100K']:.2f} ms")
print(f"  Latency (510K):   {latency_results['500K']:.2f} ms")
print()
print(f"  Read (Small):     {read_times[0]:.4f} s")
print(f"  Read (Medium):    {read_times[1]:.4f} s")
print(f"  Read (Large):     {read_times[2]:.4f} s")
print()
print(f"  Write (Small):    {write_times[0]:.4f} s")
print(f"  Write (Medium):   {write_times[1]:.4f} s")
print(f"  Write (Large):    {write_times[2]:.4f} s")
print()
print(f"  Query (Small):    {query_times[0]:.4f} s")
print(f"  Query (Medium):   {query_times[1]:.4f} s")
print(f"  Query (Large):    {query_times[2]:.4f} s")
print("=" * 60)
print("\nInteresting Observations:")
print("  • Latency IMPROVED with larger datasets (22.92 → 7.03 → 8.56 ms)")
print("  • Read performance IMPROVED with more data (0.0043 → 0.0026 → 0.0020 s)")
print("  • Write performance IMPROVED significantly (0.0968 → 0.0821 → 0.0349 s)")
print("  • Query times stayed consistently low (< 0.01 s)")
print("\n  This suggests CockroachDB optimizes better with larger datasets!")
print("=" * 60)

plt.show()