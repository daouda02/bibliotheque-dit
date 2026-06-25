from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from app.models import Livre
from app.serializers import LivreSerializer, LivreListSerializer


class LivreListCreateView(APIView):
    """
    GET  /api/livres/        — liste tous les livres (paginée)
    POST /api/livres/        — ajouter un livre
    """

    def get(self, request):
        livres = Livre.objects.all()
        serializer = LivreListSerializer(livres, many=True)
        return Response({
            'count': livres.count(),
            'results': serializer.data
        })

    def post(self, request):
        serializer = LivreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LivreDetailView(APIView):
    """
    GET    /api/livres/<id>/  — détail d'un livre
    PUT    /api/livres/<id>/  — modifier complètement
    PATCH  /api/livres/<id>/  — modifier partiellement
    DELETE /api/livres/<id>/  — supprimer
    """

    def get(self, request, pk):
        livre = get_object_or_404(Livre, pk=pk)
        serializer = LivreSerializer(livre)
        return Response(serializer.data)

    def put(self, request, pk):
        livre = get_object_or_404(Livre, pk=pk)
        serializer = LivreSerializer(livre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        livre = get_object_or_404(Livre, pk=pk)
        serializer = LivreSerializer(livre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        livre = get_object_or_404(Livre, pk=pk)
        livre.delete()
        return Response(
            {'message': f'Livre "{livre.titre}" supprimé avec succès'},
            status=status.HTTP_204_NO_CONTENT
        )


class LivreRechercheView(APIView):
    """
    GET /api/livres/recherche/?q=<terme>  — recherche par titre, auteur ou ISBN
    GET /api/livres/recherche/?genre=<g>  — filtrer par genre
    """

    def get(self, request):
        q = request.query_params.get('q', '')
        genre = request.query_params.get('genre', '')

        livres = Livre.objects.all()

        if q:
            livres = livres.filter(
                Q(titre__icontains=q) |
                Q(auteur__icontains=q) |
                Q(isbn__icontains=q)
            )
        if genre:
            livres = livres.filter(genre__icontains=genre)

        serializer = LivreListSerializer(livres, many=True)
        return Response({
            'count': livres.count(),
            'query': q,
            'results': serializer.data
        })


class LivreDisponibiliteView(APIView):
    """
    GET  /api/livres/<id>/disponibilite/  — vérifier la disponibilité
    POST /api/livres/<id>/disponibilite/  — mettre à jour les exemplaires (usage interne)
    """

    def get(self, request, pk):
        livre = get_object_or_404(Livre, pk=pk)
        return Response({
            'id': livre.id,
            'titre': livre.titre,
            'nombre_exemplaires': livre.nombre_exemplaires,
            'exemplaires_disponibles': livre.exemplaires_disponibles,
            'est_disponible': livre.est_disponible()
        })

    def post(self, request, pk):
        """Appelé par le service Emprunts pour mettre à jour les exemplaires"""
        livre = get_object_or_404(Livre, pk=pk)
        action = request.data.get('action')  # 'emprunter' ou 'retourner'

        if action == 'emprunter':
            if not livre.est_disponible():
                return Response(
                    {'error': 'Aucun exemplaire disponible'},
                    status=status.HTTP_409_CONFLICT
                )
            livre.exemplaires_disponibles -= 1
            livre.save()
            return Response({'message': 'Exemplaire réservé', 'disponibles': livre.exemplaires_disponibles})

        elif action == 'retourner':
            if livre.exemplaires_disponibles < livre.nombre_exemplaires:
                livre.exemplaires_disponibles += 1
                livre.save()
            return Response({'message': 'Exemplaire rendu', 'disponibles': livre.exemplaires_disponibles})

        return Response({'error': 'Action invalide. Utilisez "emprunter" ou "retourner"'},
                        status=status.HTTP_400_BAD_REQUEST)
