from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from authentication.serializers import SignUpSerializer, LoginSerializer, UserSerializer

User = get_user_model()

class SignUpView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'message': "L'utilisateur a été créé avec succès.",
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }},
                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView

class LoginView(APIView):
    
    # n'importe quel utilisateur peut accéder à cette vue
    # allow any : autoriser tout
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        # un fois que c'est validé "is_valid", les données sont automatiquement stockés dans validated_data
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Si tout est correct, générer les tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

