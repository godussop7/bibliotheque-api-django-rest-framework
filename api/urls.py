from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AuteurViewSet, LivreViewSet, TagViewSet, 
    ProfilLecteurViewSet, EmpruntViewSet
)

# Création du router
router = DefaultRouter()

# Enregistrement des ViewSets avec leurs noms de base
router.register(r'auteurs', AuteurViewSet, basename='auteur')
router.register(r'livres', LivreViewSet, basename='livre')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'profils-lecteurs', ProfilLecteurViewSet, basename='profil-lecteur')
router.register(r'emprunts', EmpruntViewSet, basename='emprunt')

# URLs de l'application API
urlpatterns = [
    # URLs du router (tous les endpoints CRUD)
    path('', include(router.urls)),
    
    # Endpoints JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
