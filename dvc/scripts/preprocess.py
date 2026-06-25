"""
Étape 1 DVC : nettoyage des données d'emprunts
"""
import pandas as pd
import os

INPUT = 'dvc/data/loans.csv'
OUTPUT = 'dvc/data/loans_clean.csv'

def preprocess():
    print(f"Chargement de {INPUT}...")
    df = pd.read_csv(INPUT)
    print(f"  Lignes initiales : {len(df)}")

    # Supprimer les doublons
    df = df.drop_duplicates()

    # Supprimer les lignes avec valeurs manquantes essentielles
    df = df.dropna(subset=['utilisateur_id', 'livre_id'])

    # Convertir les types
    df['utilisateur_id'] = df['utilisateur_id'].astype(int)
    df['livre_id'] = df['livre_id'].astype(int)

    # Garder uniquement les colonnes utiles pour le ML
    df = df[['utilisateur_id', 'livre_id', 'statut', 'date_emprunt']]

    # Encoder le statut : emprunts retournés = interaction positive confirmée
    df['rating'] = df['statut'].apply(lambda x: 1.5 if x == 'retourne' else 1.0)

    print(f"  Lignes après nettoyage : {len(df)}")
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    print(f"Données nettoyées sauvegardées dans {OUTPUT}")

if __name__ == '__main__':
    preprocess()
