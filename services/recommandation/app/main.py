from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import Recommender
import os

app = FastAPI(
    title="Service de Recommandation — Bibliothèque DIT",
    description="API de recommandation de livres basée sur l'historique des emprunts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = Recommender()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": recommender.model_loaded}

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, n: int = 5):
    """Retourne les n livres recommandés pour un utilisateur"""
    if not recommender.model_loaded:
        raise HTTPException(status_code=503, detail="Modèle non disponible. Lancez /train d'abord.")
    try:
        recommendations = recommender.recommend(user_id, n=n)
        return {
            "utilisateur_id": user_id,
            "recommendations": recommendations,
            "count": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/train")
def train_model():
    try:
        metrics = recommender.train()
        recommender._load_model()  # ← forcer le rechargement après entraînement
        return {"message": "Modèle entraîné avec succès", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur entraînement : {str(e)}")
    
@app.get("/model/info")
def model_info():
    """Informations sur le modèle actuel"""
    return recommender.get_info()
