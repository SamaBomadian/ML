import pandas as pd
import requests
import time
from urllib.parse import quote

INPUT_FILE = r"E:\subjects\DDI project\dataset\db_drug_interactions.csv"
OUTPUT_FILE = r"E:\subjects\DDI project\dataset\drug_smiles.csv"

def get_smiles_from_pubchem(drug_name):
    encoded_name = quote(str(drug_name).strip())
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/property/ConnectivitySMILES/JSON"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            props = data.get("PropertyTable", {}).get("Properties", [])
            if props and "ConnectivitySMILES" in props[0]:
                return props[0]["ConnectivitySMILES"]
    except Exception:
        return None

    return None

def main():
    df = pd.read_csv(INPUT_FILE)
    df.columns = ['drug1', 'drug2', 'interaction_description']
    df = df.dropna().drop_duplicates()

    all_drugs = sorted(set(df['drug1']).union(set(df['drug2'])))

    results = []

    for i, drug in enumerate(all_drugs, start=1):
        print(f"[{i}/{len(all_drugs)}] Searching SMILES for: {drug}")
        smiles = get_smiles_from_pubchem(drug)
        results.append({
            "drug_name": drug,
            "smiles": smiles
        })
        time.sleep(0.2)

    smiles_df = pd.DataFrame(results)
    smiles_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved SMILES dataset to: {OUTPUT_FILE}")
    print(smiles_df.head(10))
    print("\nMissing SMILES:", smiles_df['smiles'].isna().sum())

if __name__ == "__main__":
    main()
