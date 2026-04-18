from django.contrib import admin
from grappelli.dashboard import Dashboard, AppIndexDashboard
from grappelli.dashboard.utils import get_admin_site
from grappelli.dashboard.models import *
from api.models import Livre, Auteur, Emprunt, ProfilLecteur

class CustomDashboard(Dashboard):
    """
    Dashboard personnalisé pour Bibliothèque API
    """
    title = 'Bibliothèque API Dashboard'
    template = 'grappelli/dashboard/dashboard.html'
    columns = 3

    def init_with_context(self, context):
        # Statistiques réelles
        total_livres = Livre.objects.count()
        total_auteurs = Auteur.objects.count()
        total_emprunts = Emprunt.objects.count()
        lecteurs_actifs = ProfilLecteur.objects.count()

        self.children.append(ModulesGroup(
            title='Statistiques',
            collapsible=True,
            children=[
                DashboardModule(
                    title='Livres',
                    template='dashboard_modules/statistiques_livres.html',
                    columns=3,
                    order=1,
                    context={
                        'total_livres': total_livres,
                        'total_auteurs': total_auteurs,
                        'total_emprunts': total_emprunts,
                        'lecteurs_actifs': lecteurs_actifs,
                    }
                ),
            ]
        ))

        self.children.append(ModulesGroup(
            title='Gestion Rapide',
            collapsible=True,
            children=[
                AppList(
                    title='Livres et Auteurs',
                    exclude=('django.contrib.*',),
                    models=('api.Livre', 'api.Auteur', 'api.Tag'),
                    columns=3,
                    order=2
                ),
                AppList(
                    title='Emprunts et Lecteurs',
                    exclude=('django.contrib.*',),
                    models=('api.Emprunt', 'api.ProfilLecteur'),
                    columns=3,
                    order=3
                ),
            ]
        ))

        self.children.append(ModulesGroup(
            title='Administration',
            collapsible=True,
            children=[
                ModelList(
                    title='Utilisateurs',
                    models=('auth.user',),
                    columns=3,
                    order=4
                ),
                RecentActions(
                    title='Actions Récentes',
                    limit=5,
                    columns=3,
                    order=5
                ),
            ]
        ))

        self.children.append(ModulesGroup(
            title='Liens Rapides',
            collapsible=True,
            children=[
                LinkList(
                    title='Liens',
                    layout='inline',
                    children=[
                        {
                            'title': 'API Documentation',
                            'url': '/api/',
                            'external': False,
                        },
                        {
                            'title': 'GitHub Repository',
                            'url': 'https://github.com/godussop7/bibliotheque-api-django-rest-framework',
                            'external': True,
                        },
                    ],
                    columns=3,
                    order=6
                ),
            ]
        ))
