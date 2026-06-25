from django.urls import path
from app.views import (
    EmpruntListCreateView, EmpruntDetailView, EmpruntRetourView,
    EmpruntHistoriqueUtilisateurView, EmpruntRetardsView, EmpruntExportCSVView
)

urlpatterns = [
    path('emprunts/', EmpruntListCreateView.as_view(), name='emprunt-list-create'),
    path('emprunts/<int:pk>/', EmpruntDetailView.as_view(), name='emprunt-detail'),
    path('emprunts/<int:pk>/retour/', EmpruntRetourView.as_view(), name='emprunt-retour'),
    path('emprunts/utilisateur/<int:utilisateur_id>/', EmpruntHistoriqueUtilisateurView.as_view(), name='emprunt-historique'),
    path('emprunts/retards/', EmpruntRetardsView.as_view(), name='emprunt-retards'),
    path('emprunts/export/', EmpruntExportCSVView.as_view(), name='emprunt-export'),
]
