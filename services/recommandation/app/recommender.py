import os
import joblib
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from datetime import datetime

MODEL_PATH = os.getenv('MODEL_PATH', '/app/model_artifacts/model.pkl')
DATA_PATH = os.getenv('DATA_PATH', '/app/model_artifacts/loans.csv')


class Recommender:
    def __init__(self):
        self.model = None
        self.livre_ids = []
        self.utilisateur_ids = []
        self.matrix = None
        self.model_loaded = False
        self.trained_at = None
        self._load_model()

    def _load_model(self):
        """Charge le modèle depuis le disque si disponible"""
        if os.path.exists(MODEL_PATH):
            try:
                data = joblib.load(MODEL_PATH)
                self.model = data['model']
                self.livre_ids = data['livre_ids']
                self.utilisateur_ids = data['utilisateur_ids']
                self.matrix = data['matrix']
                self.trained_at = data.get('trained_at')
                self.model_loaded = True
            except Exception:
                self.model_loaded = False

    def train(self):
        """Entraîne le modèle KNN sur l'historique des emprunts"""
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Fichier de données introuvable : {DATA_PATH}")

        df = pd.read_csv(DATA_PATH)
        df = df[['utilisateur_id', 'livre_id']].dropna()
        df['rating'] = 1  # Emprunt = intérêt implicite

        # Matrice utilisateur-livre
        user_book_matrix = df.pivot_table(
            index='utilisateur_id',
            columns='livre_id',
            values='rating',
            aggfunc='sum',
            fill_value=0
        )

        self.utilisateur_ids = list(user_book_matrix.index)
        self.livre_ids = list(user_book_matrix.columns)
        self.matrix = csr_matrix(user_book_matrix.values)

        # Modèle KNN (filtrage collaboratif)
        self.model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)
        self.model.fit(self.matrix)
        self.trained_at = datetime.now().isoformat()
        self.model_loaded = True

        # Sauvegarder
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'livre_ids': self.livre_ids,
            'utilisateur_ids': self.utilisateur_ids,
            'matrix': self.matrix,
            'trained_at': self.trained_at
        }, MODEL_PATH)

        return {
            'utilisateurs': len(self.utilisateur_ids),
            'livres': len(self.livre_ids),
            'trained_at': self.trained_at
        }

    def recommend(self, user_id: int, n: int = 5):
        """Recommande n livres pour un utilisateur"""
        if user_id not in self.utilisateur_ids:
            # Utilisateur inconnu : recommandations populaires
            return self._popular_books(n)

        user_idx = self.utilisateur_ids.index(user_id)
        user_vector = self.matrix[user_idx]

        distances, indices = self.model.kneighbors(user_vector, n_neighbors=min(6, self.matrix.shape[0]))

        # Livres déjà empruntés par l'utilisateur
        deja_empruntes = set(
            self.livre_ids[i] for i in range(self.matrix.shape[1])
            if user_vector[0, i] > 0
        )

        # Agréger les livres des utilisateurs similaires
        scores = {}
        for i, voisin_idx in enumerate(indices[0][1:]):  # Exclure lui-même
            poids = 1 - distances[0][i + 1]
            voisin_vector = self.matrix[voisin_idx].toarray()[0]
            for j, score in enumerate(voisin_vector):
                if score > 0:
                    livre_id = self.livre_ids[j]
                    if livre_id not in deja_empruntes:
                        scores[livre_id] = scores.get(livre_id, 0) + poids * score

        recommandations = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return [{'livre_id': int(lid), 'score': round(float(s), 4)} for lid, s in recommandations]

    def _popular_books(self, n: int):
        """Livres les plus empruntés (pour les nouveaux utilisateurs)"""
        if self.matrix is None:
            return []
        totaux = np.array(self.matrix.sum(axis=0)).flatten()
        top_indices = totaux.argsort()[-n:][::-1]
        return [{'livre_id': int(self.livre_ids[i]), 'score': float(totaux[i])} for i in top_indices]

    def get_info(self):
        return {
            'model_loaded': self.model_loaded,
            'trained_at': self.trained_at,
            'nb_utilisateurs': len(self.utilisateur_ids),
            'nb_livres': len(self.livre_ids),
            'algorithme': 'KNN (cosine similarity)'
        }
