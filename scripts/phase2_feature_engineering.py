import pandas as pd
import sqlite3
import numpy as np
import os

# 1. BIOCHEMICAL PROPERTIES
AA_PROPS = {
    'A': {'hydro': 1.8,  'mw': 89.1,  'pi': 6.00}, 'R': {'hydro': -4.5, 'mw': 174.2, 'pi': 10.76},
    'N': {'hydro': -3.5, 'mw': 132.1, 'pi': 5.41}, 'D': {'hydro': -3.5, 'mw': 133.1, 'pi': 2.77},
    'C': {'hydro': 2.5,  'mw': 121.2, 'pi': 5.07}, 'Q': {'hydro': -3.5, 'mw': 146.2, 'pi': 5.65},
    'E': {'hydro': -3.5, 'mw': 147.1, 'pi': 3.22}, 'G': {'hydro': -0.4, 'mw': 75.1,  'pi': 5.97},
    'H': {'hydro': -3.2, 'mw': 155.2, 'pi': 7.59}, 'I': {'hydro': 4.5,  'mw': 131.2, 'pi': 6.02},
    'L': {'hydro': 3.8,  'mw': 131.2, 'pi': 5.98}, 'K': {'hydro': -3.9, 'mw': 146.2, 'pi': 9.74},
    'M': {'hydro': 1.9,  'mw': 149.2, 'pi': 5.74}, 'F': {'hydro': 2.8,  'mw': 165.2, 'pi': 5.48},
    'P': {'hydro': -1.6, 'mw': 115.1, 'pi': 6.30}, 'S': {'hydro': -0.8, 'mw': 105.1, 'pi': 5.68},
    'T': {'hydro': -0.7, 'mw': 119.1, 'pi': 5.60}, 'W': {'hydro': -0.9, 'mw': 204.2, 'pi': 5.89},
    'Y': {'hydro': -1.3, 'mw': 181.2, 'pi': 5.66}, 'V': {'hydro': 4.2,  'mw': 117.1, 'pi': 5.96}
}

def run_phase_2():
    db_path = 'protein_analytics.db'
    conn = sqlite3.connect(db_path)
    
    print(f"Reading from: {os.path.abspath(db_path)}")
    
    # Define the column name clearly
    SEQUENCE_COLUMN = 'fasta_sequence'
    
    # 1. Read the data
    try:
        df_seqs = pd.read_sql(f"SELECT uniprot_id, {SEQUENCE_COLUMN} FROM raw_sequences", conn)
    except Exception as e:
        print(f"❌ Error: Database query failed. Ensure column '{SEQUENCE_COLUMN}' exists. {e}")
        return

    mutation_results = []
    valid_aas = set(AA_PROPS.keys())

    # 2. Process each protein
    for _, row in df_seqs.iterrows():
        raw_seq = str(row[SEQUENCE_COLUMN]).upper()
        pid = row['uniprot_id']
        
        print(f"Generating mutations for {pid}...")
        
        for _ in range(100):
            if len(raw_seq) < 10: continue
            
            pos = np.random.randint(0, len(raw_seq))
            wild_aa = raw_seq[pos]
            mutant_aa = np.random.choice(list(valid_aas))
            
            if wild_aa in valid_aas and wild_aa != mutant_aa:
                # Calculate the Deltas (Biochem Essence)
                d_hydro = AA_PROPS[mutant_aa]['hydro'] - AA_PROPS[wild_aa]['hydro']
                d_mw = AA_PROPS[mutant_aa]['mw'] - AA_PROPS[wild_aa]['mw']
                d_pi = AA_PROPS[mutant_aa]['pi'] - AA_PROPS[wild_aa]['pi']
                
                mutation_results.append({
                    'uniprot_id': pid,
                    'mutation': f"{wild_aa}{pos}{mutant_aa}",
                    'delta_hydro': d_hydro,
                    'delta_mw': d_mw,
                    'delta_pi': d_pi
                })

    # 3. Save the results
    if mutation_results:
        df_features = pd.DataFrame(mutation_results)
        df_features.to_sql('mutation_features', conn, if_exists='replace', index=False)
        conn.commit()
        print(f"✅ SUCCESS: {len(df_features)} mutations saved to 'mutation_features' table.")
    else:
        print("❌ No mutations generated. Check sequence validity.")

    conn.close()

if __name__ == "__main__":
    run_phase_2()