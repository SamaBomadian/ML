import pandas as pd

# File paths
INTERACTIONS_FILE = r"E:\subjects\DDI project\dataset\db_drug_interactions.csv"
SMILES_FILE = r"E:\subjects\DDI project\dataset\drug_smiles.csv"
OUTPUT_FILE = r"E:\subjects\DDI project\dataset\ddi_with_smiles.csv"

def main():
    # Load interaction dataset
    ddi_df = pd.read_csv(INTERACTIONS_FILE)
    ddi_df.columns = ['drug1', 'drug2', 'interaction_description']
    ddi_df = ddi_df.dropna().drop_duplicates()

    # Load smiles dataset
    smiles_df = pd.read_csv(SMILES_FILE)

    # Rename for merging
    smiles1_df = smiles_df.rename(columns={
        'drug_name': 'drug1',
        'smiles': 'smiles1'
    })

    smiles2_df = smiles_df.rename(columns={
        'drug_name': 'drug2',
        'smiles': 'smiles2'
    })

    # Merge smiles for drug1
    merged_df = ddi_df.merge(smiles1_df, on='drug1', how='left')

    # Merge smiles for drug2
    merged_df = merged_df.merge(smiles2_df, on='drug2', how='left')

    # Count missing
    print("Total rows before dropping missing SMILES:", len(merged_df))
    print("Missing smiles1:", merged_df['smiles1'].isna().sum())
    print("Missing smiles2:", merged_df['smiles2'].isna().sum())

    # Drop rows where either drug has missing SMILES
    merged_df = merged_df.dropna(subset=['smiles1', 'smiles2'])

    print("Total rows after dropping missing SMILES:", len(merged_df))
    print("\nSample data:")
    print(merged_df.head())

    # Save output
    merged_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved merged dataset to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
