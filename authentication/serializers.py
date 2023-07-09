from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Le serializer UserSerializer est utilisé pour la sérialisation 
    et la désérialisation des instances de User.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SignUpSerializer(serializers.ModelSerializer):
    """
    Le serializer SignUpSerializer est utilisé pour créer une nouvelle 
    instance de User en validant les données fournies par l'utilisateur.
    """
    
    # Deuxième mot de passe demandé pour confirmer le mot de passe lors de l'inscription.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        """ 
        Les champs password et password2 seront acceptés lors de la création d'un nouvel utilisateur, 
        mais ne seront pas renvoyés lors de la sérialisation de l'instance utilisateur grâce à "write_only=True.
        """
        model = User
        fields = ['username', 'email', 'password', 'password2']
        
        # Le dictionnaire extra_kwargs permet de donner des instructions plus spécifiques pour les champs ci-dessous.
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': [UniqueValidator(queryset=User.objects.all(), message="Cet email existe déjà")]}
        }

    def validate(self, data):
        """
        Vérifie si les deux mots de passe correspondent.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Les deux mots de passe ne correspondent pas."})
        return data

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec les données validées.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Le serializer LoginSerializer est utilisé pour valider les informations 
    d'identification lors de la connexion.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Vérifie si les informations d'identification sont valides.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError('Les informations d\'identification fournies ne permettent pas de se connecter.')
            if not user.is_active:
                raise serializers.ValidationError('L\'utilisateur est inactif.')
        else:
            raise serializers.ValidationError('Les champs "nom d\'utilisateur" et "mot de passe" sont nécessaires pour se connecter.')

        attrs['user'] = user
        return attrs
