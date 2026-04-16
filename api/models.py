from django.db import models
from django.contrib.auth.models import User


class Auteur(models.Model):
    nom = models.CharField(max_length=200)
    biographie = models.TextField(blank=True)
    nationalite = models.CharField(max_length=100, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Livre(models.Model):
    CATEGORIES = [
        ('roman', 'Roman'),
        ('essai', 'Essai'),
        ('poesie', 'Poésie'),
        ('theatre', 'Théâtre'),
        ('science', 'Science'),
        ('autre', 'Autre'),
    ]
    
    titre = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    annee_publication = models.IntegerField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name='livres')
    tags = models.ManyToManyField(Tag, blank=True, related_name='livres')
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} ({self.auteur.nom})"


class ProfilLecteur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    date_adhesion = models.DateField(auto_now_add=True)
    livres_empruntes_max = models.IntegerField(default=5)
    telephone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"Profil de {self.utilisateur.username}"


class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts')
    lecteur = models.ForeignKey(ProfilLecteur, on_delete=models.CASCADE, related_name='emprunts')
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(null=True, blank=True)
    rendu = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_emprunt']

    def __str__(self):
        return f"{self.lecteur.utilisateur.username} - {self.livre.titre}"
