from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from app.models import Utilisateur
from app.serializers import UtilisateurSerializer, UtilisateurListSerializer


class UtilisateurListCreateView(APIView):
    """GET /api/utilisateurs/ — POST /api/utilisateurs/"""

    def get(self, request):
        type_u = request.query_params.get('type', '')
        utilisateurs = Utilisateur.objects.all()
        if type_u:
            utilisateurs = utilisateurs.filter(type_utilisateur=type_u)
        serializer = UtilisateurListSerializer(utilisateurs, many=True)
        return Response({'count': utilisateurs.count(), 'results': serializer.data})

    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UtilisateurDetailView(APIView):
    """GET/PUT/PATCH/DELETE /api/utilisateurs/<id>/"""

    def get(self, request, pk):
        u = get_object_or_404(Utilisateur, pk=pk)
        return Response(UtilisateurSerializer(u).data)

    def put(self, request, pk):
        u = get_object_or_404(Utilisateur, pk=pk)
        serializer = UtilisateurSerializer(u, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        u = get_object_or_404(Utilisateur, pk=pk)
        serializer = UtilisateurSerializer(u, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        u = get_object_or_404(Utilisateur, pk=pk)
        u.delete()
        return Response({'message': 'Utilisateur supprimé'}, status=status.HTTP_204_NO_CONTENT)


class UtilisateurRechercheView(APIView):
    """GET /api/utilisateurs/recherche/?q=<terme>"""

    def get(self, request):
        q = request.query_params.get('q', '')
        utilisateurs = Utilisateur.objects.all()
        if q:
            utilisateurs = utilisateurs.filter(
                Q(nom__icontains=q) |
                Q(prenom__icontains=q) |
                Q(email__icontains=q) |
                Q(numero_carte__icontains=q)
            )
        serializer = UtilisateurListSerializer(utilisateurs, many=True)
        return Response({'count': utilisateurs.count(), 'results': serializer.data})


class UtilisateurProfilView(APIView):
    """GET /api/utilisateurs/<id>/profil/ — profil complet avec stats"""

    def get(self, request, pk):
        u = get_object_or_404(Utilisateur, pk=pk)
        data = UtilisateurSerializer(u).data
        data['stats'] = {
            'type_label': dict(Utilisateur.TYPE_CHOICES).get(u.type_utilisateur, ''),
            'compte_actif': u.actif,
        }
        return Response(data)


class UtilisateurActivationView(APIView):
    """PATCH /api/utilisateurs/<id>/activation/ — activer/désactiver"""

    def patch(self, request, pk):
        u = get_object_or_404(Utilisateur, pk=pk)
        u.actif = not u.actif
        u.save()
        etat = 'activé' if u.actif else 'désactivé'
        return Response({'message': f'Utilisateur {etat}', 'actif': u.actif})
