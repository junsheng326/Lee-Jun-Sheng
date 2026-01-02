from pymongo import MongoClient
import time
import matplotlib.pyplot as plt

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['LatencyScalabilityTest']  # ← Change this!

# Your three collections with different sizes
collections = {
    'small_dataset': db['DBMS'],
    'medium_dataset': db['DBMS01'],
    'large_dataset': db['DBMS02']
}

# Store results
results = {
    'dataset_names': [],
    'doc_counts': [],
    'read_times': [],
    'write_times': [],
    'query_times': []
}

print("Starting MongoDB Scalability Test...\n")

for name, collection in collections.items():
    print(f"Testing: {name}")
    
    # Count documents
    doc_count = collection.count_documents({})
    print(f"  Documents: {doc_count}")
    
    # Test 1: Read Performance (fetch 100 documents and actually access them)
    start = time.time()
    docs = list(collection.find().limit(100))
    # Actually access the documents to ensure they're loaded
    for doc in docs:
        _ = doc.get('_id')
    read_time = time.time() - start
    docs_read = len(docs)
    print(f"  Read {docs_read} docs: {read_time:.4f} seconds")
    
    # Test 2: Write Performance (insert 10 documents)
    start = time.time()
    test_docs = [{'test': i, 'timestamp': time.time()} for i in range(10)]
    collection.insert_many(test_docs)
    write_time = time.time() - start
    print(f"  Write 10 docs: {write_time:.4f} seconds")
    
    # Test 3: Query Performance (find with condition)
    start = time.time()
    # Adjust this query to match your actual data structure
    query_results = list(collection.find({'test': {'$exists': True}}).limit(50))
    query_time = time.time() - start
    print(f"  Query 50 docs: {query_time:.4f} seconds")
    
    # Clean up test documents
    collection.delete_many({'test': {'$exists': True}})
    
    # Store results
    results['dataset_names'].append(name)
    results['doc_counts'].append(doc_count)
    results['read_times'].append(read_time)
    results['write_times'].append(write_time)
    results['query_times'].append(query_time)
    
    print()

    # Visualize Results
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('MongoDB Scalability Test Results', fontsize=16)

# Plot 1: Document Counts
axes[0, 0].bar(results['dataset_names'], results['doc_counts'], color='skyblue')
axes[0, 0].set_title('Dataset Sizes')
axes[0, 0].set_ylabel('Number of Documents')
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Read Performance
axes[0, 1].plot(results['doc_counts'], results['read_times'], marker='o', color='green', linewidth=2)
axes[0, 1].set_title('Read Performance')
axes[0, 1].set_xlabel('Number of Documents')
axes[0, 1].set_ylabel('Time (seconds)')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Write Performance
axes[1, 0].plot(results['doc_counts'], results['write_times'], marker='s', color='orange', linewidth=2)
axes[1, 0].set_title('Write Performance')
axes[1, 0].set_xlabel('Number of Documents')
axes[1, 0].set_ylabel('Time (seconds)')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Query Performance
axes[1, 1].plot(results['doc_counts'], results['query_times'], marker='^', color='red', linewidth=2)
axes[1, 1].set_title('Query Performance')
axes[1, 1].set_xlabel('Number of Documents')
axes[1, 1].set_ylabel('Time (seconds)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('scalability_results.png', dpi=300, bbox_inches='tight')
plt.show()

print("Test completed! Results saved to 'scalability_results.png'")

# Print Summary
print("\n" + "="*50)
print("SUMMARY")
print("="*50)
for i, name in enumerate(results['dataset_names']):
    print(f"\n{name}:")
    print(f"  Documents: {results['doc_counts'][i]:,}")
    print(f"  Read Time: {results['read_times'][i]:.4f}s")
    print(f"  Write Time: {results['write_times'][i]:.4f}s")
    print(f"  Query Time: {results['query_times'][i]:.4f}s")