# Drug-Drug Interaction Predictor

A machine learning-based prototype for predicting potential drug-drug interactions (DDIs) using molecular structure information.

## Project Overview
This project aims to detect whether a potential interaction exists between two drugs.  
It combines:
- a **recorded interaction lookup** from the original dataset
- an **experimental SMILES-based machine learning model** for unseen drug pairs

The system was developed as an academic prototype to demonstrate how machine learning can be applied in healthcare decision-support tasks.

## Features
- Check known drug-drug interactions from the original dataset
- Predict possible interactions for unseen drug pairs
- Retrieve molecular structures (**SMILES**) from **PubChem**
- Convert SMILES into molecular fingerprints using **RDKit**
- Train a **Random Forest Classifier**
- Provide a desktop GUI built with **Tkinter**
- Show interaction descriptions when available

## Project Structure
```bash
DDI project/
├── dataset/
│   ├── db_drug_interactions.csv
│   ├── drug_smiles.csv
│   └── ddi_with_smiles.csv
│
├── code/
│   ├── build_smiles_dataset.py
│   ├── preprocess_smiles.py
│   ├── train_smiles_model.py
│   ├── gui_app_v2.py
│   └── test_pubchem.py
│
├── model/
│   ├── ddi_smiles_model.pkl
│   └── ddi_smiles_data.pkl
│
└── README.md
