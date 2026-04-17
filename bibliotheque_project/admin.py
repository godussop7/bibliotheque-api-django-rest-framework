from django.contrib import admin
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'Bibliothèque API'
    site_title = 'Bibliothèque API'
    index_title = 'Administration de la Bibliothèque'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = []
        return custom_urls + urls

custom_admin_site = CustomAdminSite(name='custom_admin')
