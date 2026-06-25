from rest_framework import serializers
from app.models import Emprunt

class EmpruntSerializer(serializers.ModelSerializer):
    est_en_retard = serializers.SerializerMethodField()
    jours_retard = serializers.SerializerMethodField()

    class Meta:
        model = Emprunt
        fields = [
            'id', 'utilisateur_id', 'livre_id',
            'date_emprunt', 'date_retour_prevue', 'date_retour_effective',
            'statut', 'note', 'est_en_retard', 'jours_retard'
        ]
        read_only_fields = ['id', 'date_emprunt', 'date_retour_prevue', 'statut']

    def get_est_en_retard(self, obj):
        return obj.est_en_retard()

    def get_jours_retard(self, obj):
        return obj.jours_retard()

class EmpruntCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprunt
        fields = ['utilisateur_id', 'livre_id', 'note']
