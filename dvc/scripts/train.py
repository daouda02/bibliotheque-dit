"""
Étape 2 DVC : entraînement du modèle KNN collaboratif
"""
import pandas as pd
import joblib
import os
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from datetime import datetime

INPUT = 'dvc/data/loans_clean.csv'
OUTPUT = 'dvc/models/model.pkl'

def train():
    print(f"Chargement de {INPUT}...")
    df = pd.read_csv(INPUT)

    # Matrice utilisateur-livre
    matrix_df = df.pivot_table(
        index='utilisateur_id',
        columns='livre_id',
        values='rating',
        aggfunc='sum',
        fill_value=0
    )

    utilisateur_ids = list(matrix_df.index)
    livre_ids = list(matrix_df.columns)
    matrix = csr_matrix(matrix_df.values)

    print(f"  Matrice : {matrix.shape[0]} utilisateurs × {matrix.shape[1]} livres")

    # Entraînement KNN
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)
    model.fit(matrix)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    joblib.dump({
        'model': model,
        'livre_ids': livre_ids,
        'utilisateur_ids': utilisateur_ids,
        'matrix': matrix,
        'trained_at': datetime.now().isoformat()
    }, OUTPUT)

    print(f"Modèle sauvegardé dans {OUTPUT}")

if __name__ == '__main__':
    train()
