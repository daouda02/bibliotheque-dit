"""
Étape 3 DVC : évaluation du modèle (précision des recommandations)
"""
import pandas as pd
import joblib
import json
import numpy as np
import os
from sklearn.model_selection import train_test_split

DATA = 'dvc/data/loans_clean.csv'
MODEL = 'dvc/models/model.pkl'
METRICS = 'dvc/metrics.json'

def evaluate():
    print("Chargement données et modèle...")
    df = pd.read_csv(DATA)
    data = joblib.load(MODEL)

    model = data['model']
    utilisateur_ids = data['utilisateur_ids']
    livre_ids = data['livre_ids']
    matrix = data['matrix']

    # Évaluation : leave-one-out sur un sous-ensemble
    users_sample = utilisateur_ids[:min(50, len(utilisateur_ids))]
    hits = 0
    total = 0

    for user_id in users_sample:
        if user_id not in utilisateur_ids:
            continue
        user_idx = utilisateur_ids.index(user_id)
        user_vector = matrix[user_idx]
        livres_empruntes = [livre_ids[i] for i in range(matrix.shape[1]) if user_vector[0, i] > 0]

        if len(livres_empruntes) < 2:
            continue

        # Simuler : cacher le dernier livre et voir si le modèle le recommande
        distances, indices = model.kneighbors(user_vector, n_neighbors=min(6, matrix.shape[0]))
        recommandes = set()
        for voisin_idx in indices[0][1:]:
            voisin_vec = matrix[voisin_idx].toarray()[0]
            for j, s in enumerate(voisin_vec):
                if s > 0:
                    recommandes.add(livre_ids[j])

        if livres_empruntes[-1] in recommandes:
            hits += 1
        total += 1

    precision = hits / total if total > 0 else 0

    # Densité de la matrice
    nb_interactions = df.shape[0]
    nb_cellules = len(utilisateur_ids) * len(livre_ids)
    densite = nb_interactions / nb_cellules if nb_cellules > 0 else 0

    metrics = {
        'precision_at_k': round(precision, 4),
        'nb_utilisateurs': len(utilisateur_ids),
        'nb_livres': len(livre_ids),
        'nb_interactions': nb_interactions,
        'densite_matrice': round(densite, 6),
        'utilisateurs_evalues': total
    }

    with open(METRICS, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"Métriques sauvegardées dans {METRICS}")
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    evaluate()
