import pandas as pd
import random
import joblib
import numpy as np

from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# File paths
INPUT_FILE = r"E:\subjects\DDI project\dataset\ddi_with_smiles.csv"
MODEL_FILE = r"E:\subjects\DDI project\model\ddi_smiles_model.pkl"
DATA_FILE = r"E:\subjects\DDI project\model\ddi_smiles_data.pkl"

def smiles_to_fingerprint(smiles, radius=2, n_bits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    arr = np.array(fp)
    return arr

def main():
    # Load dataset
    df = pd.read_csv(INPUT_FILE)
    df = df.dropna().drop_duplicates()

    # Positive samples
    df['label'] = 1

    # Create positive pairs
    positive_pairs = set()
    for _, row in df.iterrows():
        pair = tuple(sorted([row['drug1'], row['drug2']]))
        positive_pairs.add(pair)

    # Unique drugs with smiles
    drug_smiles_map = {}
    for _, row in df.iterrows():
        drug_smiles_map[row['drug1']] = row['smiles1']
        drug_smiles_map[row['drug2']] = row['smiles2']

    all_drugs = list(drug_smiles_map.keys())

    # Generate negative samples
    negative_rows = []
    negative_pairs = set()

    while len(negative_pairs) < len(positive_pairs):
        d1, d2 = random.sample(all_drugs, 2)
        pair = tuple(sorted([d1, d2]))

        if pair not in positive_pairs and pair not in negative_pairs:
            negative_pairs.add(pair)
            negative_rows.append({
                'drug1': d1,
                'drug2': d2,
                'smiles1': drug_smiles_map[d1],
                'smiles2': drug_smiles_map[d2],
                'interaction_description': 'No known interaction',
                'label': 0
            })

    neg_df = pd.DataFrame(negative_rows)

    # Combine positive and negative data
    full_df = pd.concat([df, neg_df], ignore_index=True)

    # Convert SMILES to fingerprints
    X = []
    y = []

    for _, row in full_df.iterrows():
        fp1 = smiles_to_fingerprint(row['smiles1'])
        fp2 = smiles_to_fingerprint(row['smiles2'])

        if fp1 is not None and fp2 is not None:
            combined_fp = np.concatenate([fp1, fp2])
            X.append(combined_fp)
            y.append(row['label'])

    X = np.array(X)
    y = np.array(y)

    print("Feature matrix shape:", X.shape)
    print("Labels shape:", y.shape)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train model
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)

    print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model and data
    joblib.dump(model, MODEL_FILE)
    joblib.dump(full_df, DATA_FILE)

    print(f"\nSaved model to: {MODEL_FILE}")
    print(f"Saved data to: {DATA_FILE}")

if __name__ == "__main__":
    main()
