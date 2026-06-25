import requests
import csv
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Emprunt
from app.serializers import EmpruntSerializer, EmpruntCreateSerializer


def notifier_service_livres(livre_id, action):
    """Appelle le service Livres pour mettre à jour la disponibilité"""
    try:
        url = f"{settings.LIVRES_SERVICE_URL}/api/livres/{livre_id}/disponibilite/"
        requests.post(url, json={'action': action}, timeout=5)
    except requests.RequestException:
        pass  # Log en production


class EmpruntListCreateView(APIView):
    """GET /api/emprunts/ — POST /api/emprunts/"""

    def get(self, request):
        emprunts = Emprunt.objects.all()
        statut = request.query_params.get('statut', '')
        if statut:
            emprunts = emprunts.filter(statut=statut)
        serializer = EmpruntSerializer(emprunts, many=True)
        return Response({'count': emprunts.count(), 'results': serializer.data})

    def post(self, request):
        serializer = EmpruntCreateSerializer(data=request.data)
        if serializer.is_valid():
            emprunt = serializer.save()
            notifier_service_livres(emprunt.livre_id, 'emprunter')
            return Response(EmpruntSerializer(emprunt).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpruntDetailView(APIView):
    """GET/DELETE /api/emprunts/<id>/"""

    def get(self, request, pk):
        emprunt = get_object_or_404(Emprunt, pk=pk)
        return Response(EmpruntSerializer(emprunt).data)

    def delete(self, request, pk):
        emprunt = get_object_or_404(Emprunt, pk=pk)
        emprunt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmpruntRetourView(APIView):
    """POST /api/emprunts/<id>/retour/ — retourner un livre"""

    def post(self, request, pk):
        emprunt = get_object_or_404(Emprunt, pk=pk)
        if emprunt.statut == 'retourne':
            return Response({'error': 'Ce livre a déjà été retourné'}, status=status.HTTP_400_BAD_REQUEST)
        emprunt.date_retour_effective = timezone.now()
        emprunt.statut = 'retourne'
        emprunt.save()
        notifier_service_livres(emprunt.livre_id, 'retourner')
        return Response({'message': 'Livre retourné avec succès', 'emprunt': EmpruntSerializer(emprunt).data})


class EmpruntHistoriqueUtilisateurView(APIView):
    """GET /api/emprunts/utilisateur/<id>/ — historique d'un utilisateur"""

    def get(self, request, utilisateur_id):
        emprunts = Emprunt.objects.filter(utilisateur_id=utilisateur_id)
        serializer = EmpruntSerializer(emprunts, many=True)
        return Response({'utilisateur_id': utilisateur_id, 'count': emprunts.count(), 'results': serializer.data})


class EmpruntRetardsView(APIView):
    """GET /api/emprunts/retards/ — tous les emprunts en retard"""

    def get(self, request):
        maintenant = timezone.now()
        emprunts = Emprunt.objects.filter(
            statut__in=['en_cours', 'en_retard'],
            date_retour_prevue__lt=maintenant
        )
        # Mettre à jour le statut
        emprunts.update(statut='en_retard')
        serializer = EmpruntSerializer(emprunts, many=True)
        return Response({'count': emprunts.count(), 'results': serializer.data})


class EmpruntExportCSVView(APIView):
    """GET /api/emprunts/export/ — export CSV pour le ML/DVC"""

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="loans.csv"'
        writer = csv.writer(response)
        writer.writerow(['emprunt_id', 'utilisateur_id', 'livre_id',
                         'date_emprunt', 'date_retour_prevue', 'date_retour_effective', 'statut'])
        for e in Emprunt.objects.all():
            writer.writerow([
                e.id, e.utilisateur_id, e.livre_id,
                e.date_emprunt, e.date_retour_prevue,
                e.date_retour_effective, e.statut
            ])
        return response
