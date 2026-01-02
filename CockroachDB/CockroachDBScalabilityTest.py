"""
SIMPLE CockroachDB Scalability Test - UPDATED
Tests read, write, query performance on imported data
"""

import psycopg2
import time

# Connect to database
conn = psycopg2.connect("postgresql://root@localhost:26257/defaultdb?sslmode=disable")
conn.autocommit = True
cur = conn.cursor()

# Switch to the database
cur.execute("USE latencyscalabilitytest")

# Collections to test (using lowercase names)
collections = {
    'small_dataset': 'dbms',
    'medium_dataset': 'dbms01',
    'large_dataset': 'dbms02'
}

print("Starting CockroachDB Scalability Test...\n")

# Store results
results = []

# Test each dataset
for name, table_name in collections.items():
    print(f"Testing: {name}")
    
    # Count documents
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    doc_count = cur.fetchone()[0]
    print(f"  Documents: {doc_count:,}")
    
    # Test 1: Read Performance (fetch 100 documents)
    start = time.time()
    cur.execute(f"SELECT * FROM {table_name} LIMIT 100")
    docs = cur.fetchall()
    read_time = time.time() - start
    print(f"  Read {len(docs)} docs: {read_time:.4f} seconds")
    
    # Test 2: Write Performance (insert 10 documents)
    start = time.time()
    for i in range(10):
        cur.execute(f"""
            INSERT INTO {table_name} VALUES 
            (999900{i}, 25, 'TestDept', 5, 3, 50000, 40, 'No')
        """)
    write_time = time.time() - start
    print(f"  Write 10 docs: {write_time:.4f} seconds")
    
    # Test 3: Query Performance (find with condition)
    start = time.time()
    cur.execute(f"SELECT * FROM {table_name} WHERE department = 'Finance' LIMIT 50")
    results_query = cur.fetchall()
    query_time = time.time() - start
    print(f"  Query {len(results_query)} docs: {query_time:.4f} seconds")
    
    # Clean up test documents
    cur.execute(f"DELETE FROM {table_name} WHERE employeeid >= 9999000")
    
    # Store results
    results.append({
        'name': name,
        'count': doc_count,
        'read': read_time,
        'write': write_time,
        'query': query_time
    })
    
    print()

print("Test completed!")

# Print Summary
print("\n" + "="*50)
print("SUMMARY")
print("="*50)
for r in results:
    print(f"\n{r['name']}:")
    print(f"  Documents: {r['count']:,}")
    print(f"  Read Time: {r['read']:.4f}s")
    print(f"  Write Time: {r['write']:.4f}s")
    print(f"  Query Time: {r['query']:.4f}s")

cur.close()
conn.close()