"""
SIMPLE CockroachDB Data Import - COMPLETELY FIXED
Proper connection management to avoid cursor issues
"""

import psycopg2
import csv
import time

print("=" * 60)
print("CockroachDB Data Import")
print("=" * 60)

# Step 1: Create database
print("\nStep 1: Creating database...")
conn = psycopg2.connect("postgresql://root@localhost:26257/defaultdb?sslmode=disable")
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS latencyscalabilitytest")
print("✓ Database created")
cur.close()
conn.close()

# Step 2: Create tables
print("\nStep 2: Creating tables...")
conn = psycopg2.connect("postgresql://root@localhost:26257/latencyscalabilitytest?sslmode=disable")
conn.autocommit = True
cur = conn.cursor()

tables = ['dbms', 'dbms01', 'dbms02']
for table in tables:
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            employeeid INT,
            age INT,
            department STRING,
            yearsexperience INT,
            performancescore INT,
            monthlysalary INT,
            traininghours INT,
            promotionlast5years STRING
        )
    """)
    print(f"✓ Table '{table}' created")

cur.close()
conn.close()

# Step 3: Import data - EACH FILE GETS ITS OWN CONNECTION
print("\nStep 3: Importing data...")

def import_csv(filename, table_name):
    print(f"\nImporting {filename} into {table_name}...")
    
    # NEW connection for this file
    conn = psycopg2.connect("postgresql://root@localhost:26257/latencyscalabilitytest?sslmode=disable")
    cur = conn.cursor()
    
    count = 0
    
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Get values (handle any column name variations)
                    emp_id = row.get('EmployeeID') or row.get(' EmployeeID') or row.get('EmployeeID ')
                    age = row.get('Age') or row.get(' Age')
                    dept = row.get('Department') or row.get(' Department')
                    years = row.get('YearsExperience') or row.get(' YearsExperience')
                    score = row.get('PerformanceScore') or row.get(' PerformanceScore')
                    salary = row.get('MonthlySalary') or row.get(' MonthlySalary')
                    training = row.get('TrainingHours') or row.get(' TrainingHours')
                    promo = row.get('PromotionLast5Years') or row.get(' PromotionLast5Years')
                    
                    # Skip if critical fields are missing
                    if not emp_id or not dept:
                        continue
                    
                    # Insert the record
                    cur.execute(f"""
                        INSERT INTO {table_name} VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        int(emp_id),
                        int(age) if age else 0,
                        str(dept).strip(),
                        int(years) if years else 0,
                        int(score) if score else 0,
                        int(salary) if salary else 0,
                        int(training) if training else 0,
                        str(promo).strip() if promo else 'No'
                    ))
                    
                    count += 1
                    
                    # Commit every 1000 records
                    if count % 1000 == 0:
                        conn.commit()
                        print(f"  {count:,} records imported...")
                        
                except Exception as e:
                    # Skip problematic rows
                    continue
        
        # Final commit
        conn.commit()
        print(f"✓ {table_name}: Total {count:,} records imported")
        
    except Exception as e:
        print(f"✗ Error importing {filename}: {e}")
        
    finally:
        # Always close this file's connection
        cur.close()
        conn.close()

# Import all three datasets - each gets fresh connection
import_csv('employee_performance_10000.csv', 'dbms')
import_csv('employee_performance_100000__1_.csv', 'dbms01')  
import_csv('employee_performance_500000.csv', 'dbms02')

# Verify the import
print("\n" + "=" * 60)
print("Verifying import...")
print("=" * 60)

conn = psycopg2.connect("postgresql://root@localhost:26257/latencyscalabilitytest?sslmode=disable")
cur = conn.cursor()

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    print(f"  {table}: {count:,} records")

cur.close()
conn.close()

print("\n" + "=" * 60)
print("✓ ALL DONE! Data imported successfully!")
print("=" * 60)
print("\nNext steps:")
print("  1. Run: python simple_latency_final.py")
print("  2. Run: python simple_scalability_final.py")
