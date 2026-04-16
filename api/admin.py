from django.contrib import admin
from unfold.admin import UnfoldModelAdmin
from .models import Auteur, Livre, Tag, ProfilLecteur, Emprunt


@admin.register(Auteur)
class AuteurAdmin(UnfoldModelAdmin):
    list_display = ('nom', 'nationalite', 'date_creation', 'cree_par')
    list_filter = ('nationalite', 'date_creation')
    search_fields = ('nom', 'biographie')
    readonly_fields = ('date_creation',)
    ordering = ('nom',)


@admin.register(Tag)
class TagAdmin(UnfoldModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    ordering = ('nom',)


@admin.register(Livre)
class LivreAdmin(UnfoldModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'annee_publication', 'disponible', 'date_creation')
    list_filter = ('categorie', 'disponible', 'annee_publication', 'date_creation')
    search_fields = ('titre', 'isbn', 'auteur__nom')
    readonly_fields = ('date_creation',)
    filter_horizontal = ('tags',)
    ordering = ('-date_creation',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('auteur')


@admin.register(ProfilLecteur)
class ProfilLecteurAdmin(UnfoldModelAdmin):
    list_display = ('utilisateur', 'date_adhesion', 'livres_empruntes_max', 'telephone')
    list_filter = ('date_adhesion',)
    search_fields = ('utilisateur__username', 'utilisateur__email')
    readonly_fields = ('date_adhesion',)


@admin.register(Emprunt)
class EmpruntAdmin(UnfoldModelAdmin):
    list_display = ('livre', 'lecteur', 'date_emprunt', 'date_retour_prevue', 'rendu')
    list_filter = ('rendu', 'date_emprunt', 'date_retour_prevue')
    search_fields = ('livre__titre', 'lecteur__utilisateur__username')
    readonly_fields = ('date_emprunt',)
    ordering = ('-date_emprunt',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('livre', 'lecteur__utilisateur')
