# Import pour l'administration de Django
from django.contrib import admin

# Import pour définir les routes
from django.urls import path, include

# Import pour créer des routeurs pour nos vues
from rest_framework import routers

# Import pour l'authentification avec tokens JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import pour créer des routeurs imbriqués
from rest_framework_nested import routers

# Import de nos vues
from projects.views import ProjectViewSet, IssueViewSet, CommentViewSet, UserListView
from authentication.views import SignUpView, LoginView

# On crée une instance de DefaultRouter
router = routers.DefaultRouter()

# On ajoute la vue pour l'inscription à notre routeur
router.register("signup", SignUpView, basename="signup")

# On ajoute la vue pour les projets à notre routeur
router.register('projects', ProjectViewSet, basename='projects')

# Nous créons un routeur imbriqué pour gérer les issues associées à un projet
project_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
project_router.register('issues', IssueViewSet, basename='project-issues')

# Nous créons un autre routeur imbriqué pour gérer les commentaires associés à une issue
issue_router = routers.NestedSimpleRouter(project_router, 'issues', lookup='issue')
issue_router.register('comments', CommentViewSet, basename='issue-comments')

# On définit les routes de notre application
urlpatterns = [
    # Route pour l'administration de Django
    path('admin/', admin.site.urls),
    
    # Route pour l'authentification avec Django Rest Framework
    path('api-auth/', include('rest_framework.urls')),
    
    # Route pour la connexion
    path('login/', LoginView.as_view(), name='login'),
    
    # Route pour obtenir un token JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Route pour rafraîchir un token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # On inclut les routes définies par le routeur principal
    path('', include(router.urls)),
    
    # On inclut les routes définies par le routeur de projet
    path('', include(project_router.urls)),
    
    # On inclut les routes définies par le routeur de problèmes (issues)
    path('', include(issue_router.urls)),
    
    # Route pour lister tous les utilisateurs authentifiés
    path('users/', UserListView.as_view(), name='user_list'),
]

