import pandas as pd
import sqlite3
import requests

# 0. Defining Variables
PROTEIN_IDS = ['P04637', 'P01308', 'P00698', 'P68871']
#protein ids and their names are as follows:
#1. P04637 - TP53_HUMAN (Cellular tumor antigen p53)
#2. P01308 - INS_HUMAN (Insulin)
#3. P00698 - MYG_HUMAN (Myoglobin)
#4. P68871 - HBA_HUMAN (Hemoglobin subunit alpha)

DB_NAME = 'protein_analytics.db'
protein_data = []


# 1. API to Fetch FASTA from Uniprot
def fetch_fasta_from_uniprot(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        sequence = "".join(lines[1:])
        return response.text
    else:
        raise ValueError(f"Failed to fetch FASTA for Uniprot ID: {uniprot_id}")
    


# 2. Loading Real Data to SQL Database

def run_phase1():
    # adding some important uniprot ids for reference
    PROTEIN_IDS = ['P04637', 'P01308', 'P00698', 'P68871']

    protein_data = []
print ("Fetching FASTA sequences from Uniprot...")
for pid in PROTEIN_IDS: 
        seq = fetch_fasta_from_uniprot(pid)
        if seq:
            protein_data.append({'uniprot_id': pid,  
                                 'fasta_sequence': seq,
                                 'seq_length': len(seq)
                                 })

print(f"Successfully fetched {pid} (Length: {len(seq)})")


df_proteins = pd.DataFrame(protein_data) 


# 3. Database Setup
conn = sqlite3.connect('protein_analytics.db')
df_proteins.to_sql('raw_sequences', conn, if_exists='replace', index=False)

print("\nSuccessfully created 'protein_analytics.db'")
print(pd.read_sql("SELECT uniprot_id, seq_length FROM raw_sequences", conn))
    
conn.close()

