from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Auteur, Livre, Tag, ProfilLecteur, Emprunt
from .serializers import (
    AuteurSerializer, LivreSerializer, LivreDetailSerializer,
    TagSerializer, ProfilLecteurSerializer, EmpruntSerializer, EmpruntCreateSerializer
)
from .permissions import EstProprietaireOuReadOnly
from .filters import LivreFilter
from .pagination import StandardPagination


class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all().order_by('nom')
    serializer_class = AuteurSerializer
    permission_classes = [EstProprietaireOuReadOnly]

    def perform_create(self, serializer):
        serializer.save(cree_par=self.request.user)

    @action(detail=True, methods=['get'])
    def livres(self, request, pk=None):
        """Retourne tous les livres d'un auteur"""
        auteur = self.get_object()
        livres = auteur.livres.all()
        serializer = LivreSerializer(livres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques globales sur les auteurs"""
        stats = {
            'total_auteurs': Auteur.objects.count(),
            'auteurs_avec_biographie': Auteur.objects.exclude(biographie='').count(),
            'nationalites': list(Auteur.objects.values_list('nationalite', flat=True).distinct())
        }
        return Response(stats)


class LivreViewSet(viewsets.ModelViewSet):
    queryset = (
        Livre.objects
        .select_related('auteur')    # optimise ForeignKey
        .prefetch_related('tags')    # optimise ManyToMany
        .all()
    )
    permission_classes = [EstProprietaireOuReadOnly]
    pagination_class = StandardPagination
    filterset_class = LivreFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['titre', 'auteur__nom', 'isbn']
    ordering_fields = ['titre', 'annee_publication', 'date_creation']
    ordering = ['-date_creation']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LivreDetailSerializer
        return LivreSerializer

    def perform_create(self, serializer):
        serializer.save(cree_par=self.request.user)

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Liste des livres disponibles"""
        qs = self.get_queryset().filter(disponible=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def emprunter(self, request, pk=None):
        """Emprunter un livre"""
        livre = self.get_object()
        if not livre.disponible:
            return Response(
                {'erreur': 'Ce livre n\'est pas disponible.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        livre.disponible = False
        livre.save()
        return Response({'message': f'Livre "{livre.titre}" emprunté avec succès.'})

    @action(detail=True, methods=['post'])
    def rendre(self, request, pk=None):
        """Rendre un livre"""
        livre = self.get_object()
        livre.disponible = True
        livre.save()
        return Response({'message': f'Livre "{livre.titre}" rendu avec succès.'})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('nom')
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProfilLecteurViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet en lecture seule pour les profils de lecteurs"""
    queryset = ProfilLecteur.objects.all()
    serializer_class = ProfilLecteurSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def mon_profil(self, request):
        """Retourne le profil de l'utilisateur connecté"""
        try:
            profil = ProfilLecteur.objects.get(utilisateur=request.user)
            serializer = self.get_serializer(profil)
            return Response(serializer.data)
        except ProfilLecteur.DoesNotExist:
            return Response(
                {'erreur': 'Vous n\'avez pas de profil de lecteur.'},
                status=status.HTTP_404_NOT_FOUND
            )


class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Emprunt.objects.select_related('livre', 'lecteur__utilisateur').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return EmpruntCreateSerializer
        return EmpruntSerializer

    @action(detail=False, methods=['get'])
    def mes_emprunts(self, request):
        """Retourne les emprunts de l'utilisateur connecté"""
        try:
            profil = ProfilLecteur.objects.get(utilisateur=request.user)
            emprunts = Emprunt.objects.filter(lecteur=profil)
            serializer = EmpruntSerializer(emprunts, many=True)
            return Response(serializer.data)
        except ProfilLecteur.DoesNotExist:
            return Response(
                {'erreur': 'Vous n\'avez pas de profil de lecteur.'},
                status=status.HTTP_404_NOT_FOUND
            )
