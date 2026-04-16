from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10                  # éléments par défaut
    page_size_query_param = 'size'  # ?size=20 pour surcharger
    max_page_size = 100             # maximum autorisé
