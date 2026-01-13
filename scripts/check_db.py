import sqlite3
import pandas as pd
import os

def check_data():
    db_path = 'protein_analytics.db'
    if not os.path.exists(db_path):
        print(f"❌ Error: Database file {db_path} does not exist in this folder!")
        return

    conn = sqlite3.connect(db_path)
    try:
        # Check if table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mutation_features';")
        if not cursor.fetchone():
            print("❌ Error: Table 'mutation_features' was not found in the database.")
            return

        df = pd.read_sql("SELECT * FROM mutation_features LIMIT 5", conn)
        print("✅ CHECKPOINT PASSED!")
        print(df)
    except Exception as e:
        print(f"❌ Error during check: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_data()