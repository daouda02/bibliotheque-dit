from rest_framework import serializers
from app.models import Livre

class LivreSerializer(serializers.ModelSerializer):
    est_disponible = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'auteur', 'isbn', 'editeur',
            'annee_publication', 'genre', 'description',
            'nombre_exemplaires', 'exemplaires_disponibles',
            'est_disponible', 'date_ajout', 'date_modification'
        ]
        read_only_fields = ['id', 'date_ajout', 'date_modification']

    def get_est_disponible(self, obj):
        return obj.est_disponible()

class LivreListSerializer(serializers.ModelSerializer):
    """Serializer allégé pour les listes"""
    est_disponible = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = ['id', 'titre', 'auteur', 'isbn', 'genre',
                  'exemplaires_disponibles', 'est_disponible']

    def get_est_disponible(self, obj):
        return obj.est_disponible()
