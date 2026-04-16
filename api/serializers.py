from rest_framework import serializers
from .models import Auteur, Livre, Tag, ProfilLecteur, Emprunt


class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = '__all__'
        read_only_fields = ['id', 'date_creation']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class LivreSerializer(serializers.ModelSerializer):
    # Champ calculé (non stocké en BDD, lecture seule)
    auteur_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_nom', 'disponible', 'tags'
        ]
        read_only_fields = ['id']

    def get_auteur_nom(self, obj):
        """obj = instance du Livre en cours de sérialisation"""
        return obj.auteur.nom

    def validate_isbn(self, value):
        """L'ISBN doit contenir exactement 13 chiffres"""
        # Enlever les tirets éventuels
        clean = value.replace('-', '')
        if not clean.isdigit() or len(clean) != 13:
            raise serializers.ValidationError(
                "L'ISBN doit contenir exactement 13 chiffres."
            )
        return value

    def validate_annee_publication(self, value):
        """L'année doit être dans une plage raisonnable"""
        if value < 1000 or value > 2025:
            raise serializers.ValidationError(
                "L'année doit être entre 1000 et 2025."
            )
        return value

    def validate(self, data):
        """Validation cross-champs"""
        # Exemple : les essais doivent avoir une biographie d'auteur
        if data.get('categorie') == 'essai':
            auteur = data.get('auteur')
            if auteur and not auteur.biographie:
                raise serializers.ValidationError(
                    "Les essais requièrent une biographie de l'auteur."
                )
        return data


class LivreDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur détaillé avec auteur imbriqué"""
    auteur = AuteurSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'disponible', 'tags', 'date_creation'
        ]


class ProfilLecteurSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='utilisateur.username', read_only=True)
    email = serializers.CharField(source='utilisateur.email', read_only=True)
    
    class Meta:
        model = ProfilLecteur
        fields = [
            'id', 'username', 'email', 'date_adhesion', 
            'livres_empruntes_max', 'telephone'
        ]
        read_only_fields = ['id', 'date_adhesion']


class EmpruntSerializer(serializers.ModelSerializer):
    livre_titre = serializers.CharField(source='livre.titre', read_only=True)
    lecteur_username = serializers.CharField(source='lecteur.utilisateur.username', read_only=True)
    
    class Meta:
        model = Emprunt
        fields = [
            'id', 'livre', 'livre_titre', 'lecteur', 'lecteur_username',
            'date_emprunt', 'date_retour_prevue', 'date_retour_effective', 'rendu'
        ]
        read_only_fields = ['id', 'date_emprunt']

    def validate(self, data):
        """Validation: un livre non disponible ne peut pas être emprunté"""
        livre = data.get('livre')
        if livre and not livre.disponible:
            raise serializers.ValidationError(
                "Ce livre n'est pas disponible pour l'emprunt."
            )
        return data


class EmpruntCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer un emprunt (accepte IDs simples)"""
    class Meta:
        model = Emprunt
        fields = [
            'livre', 'lecteur', 'date_retour_prevue'
        ]

    def validate(self, data):
        """Validation lors de la création"""
        livre = data.get('livre')
        if livre and not livre.disponible:
            raise serializers.ValidationError(
                "Ce livre n'est pas disponible pour l'emprunt."
            )
        return data
