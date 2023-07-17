from authentication.views import SignUpView, LoginView

from django.urls import path, include
# from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers

from projects.views import ProjectViewSet, IssueViewSet, CommentViewSet, UserListView



# On crée une instance de DefaultRouter
router = routers.DefaultRouter()

# On ajoute la vue pour l'inscription à notre routeur
# La vue SignUpView sera accessible via l'URL /signup
router.register("signup", SignUpView, basename="signup")

# On ajoute la vue pour les projets à notre routeur
# La vue ProjectViewSet sera accessible via l'URL /projects
router.register('projects', ProjectViewSet, basename='projects')

# Nous créons un routeur imbriqué pour gérer les issues associées à un projet
# On créé un routeur imbriqué pour gérer les issues associées à un projet
# Cela nous permettra d'accéder aux issues d'un projet via l'URL /projects/{project_id}/issues
project_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
project_router.register('issues', IssueViewSet, basename='project-issues')

# Nous créons un autre routeur imbriqué pour gérer les commentaires associés à une issue
# Cela nous permettra d'accéder aux commentaires d'une issue via l'URL /projects/{project_id}/issues/{issue_id}/comments
issue_router = routers.NestedSimpleRouter(project_router, 'issues', lookup='issue')
issue_router.register('comments', CommentViewSet, basename='issue-comments')

# # On définit les routes de notre application
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    # Route pour la connexion
    # La vue LoginView sera accessible via l'URL /login
    path('login/', LoginView.as_view(), name='login'),

    # Route pour obtenir un token JWT
    # La vue TokenObtainPairView sera accessible via l'URL /api/token/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Route pour rafraîchir un token JWT
    # La vue TokenRefreshView sera accessible via l'URL /api/token/refresh/
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # On inclut les routes définies par le routeur principal
    # Cela inclura toutes les vues enregistrées avec le routeur (par exemple, SignUpView et ProjectViewSet)
    path('', include(router.urls)),

    # On inclut les routes définies par le routeur de projet
    # Cela inclura toutes les vues enregistrées avec le routeur de projet (par exemple, IssueViewSet)
    path('', include(project_router.urls)),

    # On inclut les routes définies par le routeur de problèmes (issues)
    # Cela inclura toutes les vues enregistrées avec le routeur des problèmes (par exemple, CommentViewSet)
    path('', include(issue_router.urls)),

    # Route pour lister tous les utilisateurs authentifiés
    # La vue UserListView sera accessible via l'URL /users
    path('users/', UserListView.as_view(), name='user_list'),
]














# from django.contrib import admin
# from django.urls import path, include
# # from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework_nested import routers

# from projects.views import ProjectViewSet, IssueViewSet, CommentViewSet, UserListView
# from authentication.views import SignUpView, LoginView

# # On crée une instance de DefaultRouter
# router = routers.DefaultRouter()

# # On ajoute la vue pour l'inscription à notre routeur
# # La vue SignUpView sera accessible via l'URL /signup
# router.register("signup", SignUpView, basename="signup")

# # On ajoute la vue pour les projets à notre routeur
# # La vue ProjectViewSet sera accessible via l'URL /projects
# router.register('projects', ProjectViewSet, basename='projects')

# # On créé un routeur imbriqué pour gérer les issues associées à un projet
# # Cela nous permettra d'accéder aux issues d'un projet via l'URL /projects/{project_id}/issues
# project_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
# project_router.register('issues', IssueViewSet, basename='project-issues')



# # Nous créons un autre routeur imbriqué pour gérer les commentaires associés à une issue
# # Cela nous permettra d'accéder aux commentaires d'une issue via l'URL /projects/{project_id}/issues/{issue_id}/comments
# issue_router = routers.NestedSimpleRouter(project_router, 'issues', lookup='issue')
# issue_router.register('comments', CommentViewSet, basename='issue-comments')

# # On définit les routes de notre application
# urlpatterns = [
#     # Route pour l'administration de Django
#     path('admin/', admin.site.urls),
    
#     # Route pour l'authentification avec Django Rest Framework
#     path('api-auth/', include('rest_framework.urls')),
    
#     # Route pour la connexion
#     # La vue LoginView sera accessible via l'URL /login
#     path('login/', LoginView.as_view(), name='login'),
    
#     # Route pour obtenir un token JWT
#     # La vue TokenObtainPairView sera accessible via l'URL /api/token/
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
#     # Route pour rafraîchir un token JWT
#     # La vue TokenRefreshView sera accessible via l'URL /api/token/refresh/
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
#     # On inclut les routes définies par le routeur principal
#     # Cela inclura toutes les vues enregistrées avec le routeur (par exemple, SignUpView et ProjectViewSet)
#     path('', include(router.urls)),
    
#     # On inclut les routes définies par le routeur de projet
#     # Cela inclura toutes les vues enregistrées avec le routeur de projet (par exemple, IssueViewSet)
#     path('', include(project_router.urls)),
    
#     # On inclut les routes définies par le routeur de problèmes (issues)
#     # Cela inclura toutes les vues enregistrées avec le routeur des problèmes (par exemple, CommentViewSet)
#     path('', include(issue_router.urls)),
    
#     # Route pour lister tous les utilisateurs authentifiés
#     # La vue UserListView sera accessible via l'URL /users
#     path('users/', UserListView.as_view(), name='user_list'),
    
# ]

