from django.urls import path
from app.views import (
    UtilisateurListCreateView,
    UtilisateurDetailView,
    UtilisateurRechercheView,
    UtilisateurProfilView,
    UtilisateurActivationView
)

urlpatterns = [
    path('utilisateurs/', UtilisateurListCreateView.as_view(), name='utilisateur-list-create'),
    path('utilisateurs/<int:pk>/', UtilisateurDetailView.as_view(), name='utilisateur-detail'),
    path('utilisateurs/recherche/', UtilisateurRechercheView.as_view(), name='utilisateur-recherche'),
    path('utilisateurs/<int:pk>/profil/', UtilisateurProfilView.as_view(), name='utilisateur-profil'),
    path('utilisateurs/<int:pk>/activation/', UtilisateurActivationView.as_view(), name='utilisateur-activation'),
]
