from django.urls import path
from app.views import (
    LivreListCreateView,
    LivreDetailView,
    LivreRechercheView,
    LivreDisponibiliteView
)

urlpatterns = [
    # Endpoint 1 : liste + création
    path('livres/', LivreListCreateView.as_view(), name='livre-list-create'),

    # Endpoint 2 : détail + modification + suppression
    path('livres/<int:pk>/', LivreDetailView.as_view(), name='livre-detail'),

    # Endpoint 3 : recherche par titre, auteur, ISBN, genre
    path('livres/recherche/', LivreRechercheView.as_view(), name='livre-recherche'),

    # Endpoint 4 : disponibilité (lecture + mise à jour inter-services)
    path('livres/<int:pk>/disponibilite/', LivreDisponibiliteView.as_view(), name='livre-disponibilite'),
]
