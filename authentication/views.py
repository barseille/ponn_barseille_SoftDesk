from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from authentication.serializers import SignUpSerializer, LoginSerializer, UserSerializer

User = get_user_model()

class SignUpView(viewsets.ModelViewSet):
    """
    Vue pour l'inscription des utilisateurs.
    """
    
    # Récupère tous les utilisateurs
    queryset = User.objects.all()
    
    serializer_class = SignUpSerializer
    
    # N'importe qui peut s'inscrire
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Crée un nouvel utilisateur.
        """
        
        # Initialise une instance de SignUpSerializer avec les données de la requête
        serializer = self.get_serializer(data=request.data)
        
        # Vérifie si les données sont valides
        if serializer.is_valid(raise_exception=True):
            
            # Enregistre l'utilisateur
            user = serializer.save()

            # Crée un nouveau token de rafraîchissement pour l'utilisateur
            refresh = RefreshToken.for_user(user)
            
            # Renvoie une réponse avec les données de l'utilisateur, un message de succès et les tokens
            return Response({
                'user': UserSerializer(user).data,
                'message': "L'utilisateur a été créé avec succès.",
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }},
                status=status.HTTP_201_CREATED)

        # Si les données ne sont pas valides, renvoie une réponse avec les erreurs
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    """
    Vue pour la connexion des utilisateurs.
    """
    
    # Tout le monde peut se connecter
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Connecter un utilisateur.
        """
        
        # Initialise le serializer avec les données de la requête
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        # Vérifie si les données sont valides
        serializer.is_valid(raise_exception=True)
        
        # Récupère l'utilisateur à partir des données validées
        user = serializer.validated_data['user']

        # Génère des tokens pour l'utilisateur
        refresh = RefreshToken.for_user(user)
        
        # Renvoie une réponse avec les tokens
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

