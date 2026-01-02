import matplotlib.pyplot as plt
import numpy as np

# Data from the comparison table
datasets = [10, 100, 500]  # in thousands

# MongoDB data
mongo_latency = [17.45, 23.53, 28.79]
mongo_read = [0.0013, 0.0014, 0.0020]
mongo_write = [0.0013, 0.0014, 0.0020]
mongo_query = [0.0083, 0.0912, 0.4819]

# CockroachDB data
cockroach_latency = [22.92, 7.03, 8.56]
cockroach_read = [0.0043, 0.0026, 0.0020]
cockroach_write = [0.0968, 0.0821, 0.0082]
cockroach_query = [0.0020, 0.0349, 0.0025]

# Calculate normalized scores (0-100, higher is better)
# For each metric, calculate: score = 100 * (1 - value/max_value) for each database

def calculate_category_score(mongo_values, cockroach_values):
    """Calculate win rate for each database in a category"""
    mongo_wins = 0
    cockroach_wins = 0
    
    for m, c in zip(mongo_values, cockroach_values):
        if m < c:  # Lower is better
            mongo_wins += 1
        else:
            cockroach_wins += 1
    
    return mongo_wins, cockroach_wins

# Calculate wins for each category
mongo_latency_wins, cockroach_latency_wins = calculate_category_score(mongo_latency, cockroach_latency)
mongo_read_wins, cockroach_read_wins = calculate_category_score(mongo_read, cockroach_read)
mongo_write_wins, cockroach_write_wins = calculate_category_score(mongo_write, cockroach_write)
mongo_query_wins, cockroach_query_wins = calculate_category_score(mongo_query, cockroach_query)

# Calculate overall scores (out of 12 total tests: 3 dataset sizes × 4 metrics)
mongo_total = mongo_latency_wins + mongo_read_wins + mongo_write_wins + mongo_query_wins
cockroach_total = cockroach_latency_wins + cockroach_read_wins + cockroach_write_wins + cockroach_query_wins

# Create the visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('MongoDB vs CockroachDB Performance Summary', fontsize=16, fontweight='bold')

# Plot 1: Category-wise comparison
categories = ['Latency', 'Read Ops', 'Write Ops', 'Query Ops']
mongo_scores = [mongo_latency_wins, mongo_read_wins, mongo_write_wins, mongo_query_wins]
cockroach_scores = [cockroach_latency_wins, cockroach_read_wins, cockroach_write_wins, cockroach_query_wins]

x = np.arange(len(categories))
width = 0.35

bars1 = axes[0].bar(x - width/2, mongo_scores, width, label='MongoDB', color='#13AA52', alpha=0.8)
bars2 = axes[0].bar(x + width/2, cockroach_scores, width, label='CockroachDB', color='#6933FF', alpha=0.8)

axes[0].set_xlabel('Performance Category', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Wins (out of 3 tests)', fontsize=12, fontweight='bold')
axes[0].set_title('Category-wise Performance Wins', fontsize=13, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(categories)
axes[0].legend(fontsize=11)
axes[0].set_ylim(0, 3.5)
axes[0].grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)

# Plot 2: Overall performance score
databases = ['MongoDB', 'CockroachDB']
overall_scores = [mongo_total, cockroach_total]
colors = ['#13AA52', '#6933FF']

bars = axes[1].bar(databases, overall_scores, color=colors, alpha=0.8, width=0.5)

axes[1].set_ylabel('Total Wins (out of 12 tests)', fontsize=12, fontweight='bold')
axes[1].set_title('Overall Performance Score', fontsize=13, fontweight='bold')
axes[1].set_ylim(0, 14)
axes[1].grid(True, alpha=0.3, axis='y')

# Add value labels and percentages on bars
for i, (bar, score) in enumerate(zip(bars, overall_scores)):
    height = bar.get_height()
    percentage = (score / 12) * 100
    axes[1].text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}/12\n({percentage:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=12)

# Add winner annotation
winner = 'MongoDB' if mongo_total > cockroach_total else 'CockroachDB'
winner_color = '#13AA52' if mongo_total > cockroach_total else '#6933FF'
axes[1].text(0.5, 0.95, f'Winner: {winner}', 
            transform=axes[1].transAxes,
            ha='center', va='top',
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=winner_color, alpha=0.3))

plt.tight_layout()
plt.show()

# Print detailed summary
print("\n" + "="*60)
print("PERFORMANCE COMPARISON SUMMARY")
print("="*60)

print("\nCategory Breakdown (Wins out of 3 dataset sizes):")
print(f"  Latency:     MongoDB {mongo_latency_wins} - {cockroach_latency_wins} CockroachDB")
print(f"  Read Ops:    MongoDB {mongo_read_wins} - {cockroach_read_wins} CockroachDB")
print(f"  Write Ops:   MongoDB {mongo_write_wins} - {cockroach_write_wins} CockroachDB")
print(f"  Query Ops:   MongoDB {mongo_query_wins} - {cockroach_query_wins} CockroachDB")

print(f"\nOverall Score (out of 12 total tests):")
print(f"  MongoDB:     {mongo_total} wins ({(mongo_total/12)*100:.1f}%)")
print(f"  CockroachDB: {cockroach_total} wins ({(cockroach_total/12)*100:.1f}%)")

print(f"\n🏆 WINNER: {winner}")
print("="*60)

print("\nKey Insights:")
if mongo_write_wins > cockroach_write_wins:
    print("  ✓ MongoDB excels at write operations")
if cockroach_query_wins > mongo_query_wins:
    print("  ✓ CockroachDB excels at query operations")
if cockroach_latency_wins > mongo_latency_wins:
    print("  ✓ CockroachDB shows better latency at scale")
if mongo_read_wins > cockroach_read_wins:
    print("  ✓ MongoDB shows better read performance")