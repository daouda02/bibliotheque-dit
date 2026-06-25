from rest_framework import serializers
from app.models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    nom_complet = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = [
            'id', 'nom', 'prenom', 'nom_complet', 'email',
            'telephone', 'type_utilisateur', 'numero_carte',
            'actif', 'date_inscription', 'date_modification'
        ]
        read_only_fields = ['id', 'date_inscription', 'date_modification']

    def get_nom_complet(self, obj):
        return obj.nom_complet()

class UtilisateurListSerializer(serializers.ModelSerializer):
    nom_complet = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = ['id', 'nom_complet', 'email', 'type_utilisateur', 'numero_carte', 'actif']

    def get_nom_complet(self, obj):
        return obj.nom_complet()
