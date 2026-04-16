# API Bibliothèque - Django REST Framework

Une API REST complète pour la gestion d'une bibliothèque développée avec Django REST Framework.

## Projet réalisé dans le cadre du TP ISEP - Django REST Framework

## Fonctionnalités

### Modèles de données
- **Auteur** : nom, biographie, nationalité
- **Livre** : titre, ISBN, année de publication, catégorie, auteur, tags
- **Tag** : étiquettes pour classer les livres
- **ProfilLecteur** : profil utilisateur avec droits d'emprunt
- **Emprunt** : gestion des emprunts et retours de livres

### API REST
- **CRUD complet** sur tous les modèles
- **Authentification JWT** pour sécuriser les endpoints
- **Permissions** personnalisées (propriétaire ou lecture seule)
- **Pagination** configurable
- **Filtres avancés** : par catégorie, année, recherche texte, tri
- **Actions personnalisées** : emprunter/rendre un livre, statistiques

### Administration
- **Interface Django Admin** complète pour gérer les données
- **Superutilisateur** : admin / admin123

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd bibliotheque-api
```

2. **Créer l'environnement virtuel**
```bash
python -m venv env_bibliotheque

# Windows
env_bibliotheque\Scripts\activate

# Linux/Mac
source env_bibliotheque/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer le superutilisateur**
```bash
python manage.py createsuperuser
# Nom : admin
# Email : admin@example.com
# Mot de passe : admin123
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

## Endpoints API

### Authentification
- `POST /api/auth/token/` - Obtenir un token JWT
- `POST /api/auth/token/refresh/` - Rafraîchir le token

### Auteurs
- `GET /api/auteurs/` - Lister tous les auteurs
- `POST /api/auteurs/` - Créer un auteur (auth requis)
- `GET /api/auteurs/{id}/` - Détail d'un auteur
- `PUT /api/auteurs/{id}/` - Modifier un auteur
- `DELETE /api/auteurs/{id}/` - Supprimer un auteur
- `GET /api/auteurs/{id}/livres/` - Livres d'un auteur
- `GET /api/auteurs/stats/` - Statistiques globales

### Livres
- `GET /api/livres/` - Lister tous les livres (paginé, filtré)
- `POST /api/livres/` - Créer un livre (auth requis)
- `GET /api/livres/{id}/` - Détail d'un livre
- `PUT /api/livres/{id}/` - Modifier un livre
- `DELETE /api/livres/{id}/` - Supprimer un livre
- `GET /api/livres/disponibles/` - Livres disponibles
- `POST /api/livres/{id}/emprunter/` - Emprunter un livre
- `POST /api/livres/{id}/rendre/` - Rendre un livre

### Tags
- `GET /api/tags/` - Lister tous les tags
- `POST /api/tags/` - Créer un tag (auth requis)

### Profils Lecteurs
- `GET /api/profils-lecteurs/` - Lister les profils
- `GET /api/profils-lecteurs/mon_profil/` - Mon profil (auth requis)

### Emprunts
- `GET /api/emprunts/` - Lister tous les emprunts
- `POST /api/emprunts/` - Créer un emprunt
- `GET /api/emprunts/mes_emprunts/` - Mes emprunts (auth requis)

## Exemples d'utilisation

### Obtenir un token JWT
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "admin123"}'
```

### Créer un auteur
```bash
curl -X POST http://127.0.0.1:8000/api/auteurs/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <votre-token>' \
  -d '{"nom": "Victor Hugo", "nationalite": "Française"}'
```

### Filtrer les livres
```bash
curl -X GET "http://127.0.0.1:8000/api/livres/?categorie=roman&disponible=true&search=hugo"
```

## Filtres disponibles

### Filtres sur les livres
- `categorie` : roman, essai, poesie, theatre, science, autre
- `disponible` : true/false
- `titre` : recherche insensible à la casse
- `auteur_nom` : recherche par nom d'auteur
- `annee_min` / `annee_max` : plage d'années
- `search` : recherche dans titre, auteur, ISBN
- `ordering` : tri par titre, annee_publication, date_creation

### Pagination
- `page` : numéro de page
- `size` : nombre d'éléments par page (max 100)

## Technologies utilisées

- **Django 6.0** - Framework web
- **Django REST Framework** - API REST
- **Simple JWT** - Authentification JWT
- **Django Filter** - Filtres avancés
- **SQLite** - Base de données (développement)

## Structure du projet

```
bibliotheque_project/
|
 api/
 |   admin.py              # Interface d'administration
 |   filters.py            # Filtres personnalisés
 |   models.py             # Modèles de données
 |   pagination.py         # Configuration pagination
 |   permissions.py        # Permissions personnalisées
 |   serializers.py        # Sérialiseurs DRF
 |   urls.py               # URLs de l'API
 |   views.py              # ViewSets DRF
 |
 bibliotheque_project/
 |   settings.py           # Configuration Django
 |   urls.py               # URLs principales
 |
 manage.py
 requirements.txt
 README.md
```

## Auteur

Projet réalisé dans le cadre du TP Django REST Framework - ISEP

## License

Ce projet est utilisé à des fins pédagogiques.
