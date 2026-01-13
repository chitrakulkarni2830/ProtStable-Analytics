import pandas as pd
import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def run_phase_3():
    # 1. LOAD DATA FROM SQL
    db_path = 'protein_analytics.db'
    conn = sqlite3.connect(db_path)
    
    try:
        df = pd.read_sql("SELECT * FROM mutation_features", conn)
        print(f"Loaded {len(df)} mutations for training.")
    except Exception as e:
        print(f"❌ Error: Could not find features table. {e}")
        return

    # 2. TARGET SIMULATION (Ground Truth)
    # In a real project, this would be experimental data.
    # We model it: DDG = -0.6*(d_hydro) - 0.02*(d_mw) + noise
    # This represents the biochemical reality that hydrophobicity is a major driver of folding.
    np.random.seed(42)
    df['target_ddg'] = (df['delta_hydro'] * -0.6) + (df['delta_mw'] * -0.015) + np.random.normal(0, 0.1, len(df))

    # 3. MACHINE LEARNING PREP
    # Features (X) and Target (y)
    X = df[['delta_hydro', 'delta_mw', 'delta_pi']]
    y = df['target_ddg']

    # Split: 80% to train the model, 20% to test it
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. INITIALIZE & TRAIN THE RANDOM FOREST
    print("Training the Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. PREDICTION & EVALUATION
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\n--- MODEL PERFORMANCE ---")
    print(f"R-Squared Score: {r2:.4f}")
    print(f"Root Mean Squared Error: {rmse:.4f} kcal/mol")

    # 6. FEATURE IMPORTANCE (The 'Insight' for your portfolio)
    importances = pd.DataFrame({
        'Biochemical_Property': X.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    print("\n--- FEATURE IMPORTANCE ---")
    print(importances)

    # 7. EXPORT FINAL DATA FOR TABLEAU
    # Add predictions back to the main dataframe
    df['predicted_ddg'] = model.predict(X)
    
    # Save to CSV
    output_file = 'final_mutation_analysis.csv'
    df.to_csv(output_file, index=False)
    
    # Save to a final SQL table
    df.to_sql('final_results', conn, if_exists='replace', index=False)
    
    print(f"\n✅ SUCCESS! Final analysis exported to '{output_file}'")
    conn.close()

if __name__ == "__main__":
    run_phase_3()