from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, UserSerializer, ProjectDetailSerializer
from .permissions import IsAuthor, IsIssueAuthor, IsAuthorOrContributor, IsCommentAuthor, IsIssueAuthorOrContributor


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour la vue de l'API des objets 'Project'.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        """
        Personnalise la queryset pour renvoyer seulement les projets où 
        l'utilisateur connecté est l'auteur ou un contributeur.
        """
        user = self.request.user     
        return Project.objects.filter(Q(author=user) | Q(contributors=user)).distinct()



    def perform_create(self, serializer):
        """
        On définit l'utilisateur connecté comme auteur lors de la création d'un projet.
        """
        serializer.save(author=self.request.user)


    def get_serializer_class(self):
        """
        Retourne les détails d'un projet pour l'action 'retrieve', 
        sinon le serializer par défaut.
        """
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return self.serializer_class


    def get_permissions(self):
        """
        Surcharge de la méthode `get_permissions`
        pour assigner des permissions différentes selon l'action.
        """
        if self.action in ['update', 'partial_update', 'destroy', 'add_contributor', 'remove_contributor']:
            self.permission_classes = [IsAuthor]
        return super(ProjectViewSet, self).get_permissions()
 


    @action(detail=True, methods=['post'], url_path='users')
    def add_contributor(self, request, pk=None):
        """
        Méthode personnalisée pour ajouter un contributeur à un projet.
        """

        # Récupérer le projet actuel
        project = self.get_object()

        # Essaie de récupérer l'utilisateur avec l'ID contributor_id
        try:
            # Récupérer l'utilisateur qui doit être ajouté en tant que contributeur
            contributor_user = get_user_model().objects.get(id=request.data.get('contributor_id'))

            # Vérifier si l'utilisateur est déjà contributeur du projet
            if project.contributors.filter(id=contributor_user.id).exists():
                # Si oui, renvoyer un message d'erreur
                return Response({'message': 'Cet utilisateur est déjà un contributeur du projet.'}, status=status.HTTP_400_BAD_REQUEST)

            # Si non, créer un nouvel enregistrement dans la table des contributeurs
            Contributor.objects.create(user=contributor_user, project=project)

        
        except get_user_model().DoesNotExist:
            return Response({'message': "Le contributeur n'existe pas."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Contributeur ajouté avec succès au projet.'}, status=status.HTTP_201_CREATED)

    
    
    
    @action(detail=True, methods=['delete'], url_path='users/(?P<contributor_id>\d+)')
    def remove_contributor(self, request, pk=None, contributor_id=None):
        """
        Méthode personnalisée pour supprimer un contributeur d'un projet.
        """
        # Récupérer le projet actuel
        project = self.get_object()

        try:
            # Essayer de trouver le contributeur dans le projet
            contributor = project.project_contributors.get(user_id=contributor_id)
            # Si le contributeur existe, le supprimer
            contributor.delete()
        except Contributor.DoesNotExist:
            # Si le contributeur n'existe pas, renvoyer une erreur 404
            return Response({'message': 'Le contributeur que vous voulez supprimer n\'existe pas dans ce projet.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Contributeur supprimé avec succès du projet.'}, status=status.HTTP_204_NO_CONTENT)

 

class IssueViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour la vue de l'API des objets 'Issue'.
    """

    # Récupérer tous les problèmes
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    
    # Les permissions sont définies par défaut comme IsAuthenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Cette méthode est surchargée pour personnaliser la queryset en fonction de l'utilisateur qui fait la requête.
        """

        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user

        # Renvoyer les problèmes où l'utilisateur est l'auteur ou contributeur
        return Issue.objects.filter(Q(project__author=user) | Q(project__contributors=user))

    def perform_create(self, serializer):
        """
        Surchargée pour ajouter l'auteur et le projet lors de la création d'une issue.
        """

        # Récupérer l'ID du projet
        project_id = self.kwargs['project_pk']

        # Trouver le projet correspondant
        project = get_object_or_404(Project, pk=project_id)

        # Enregistrer la nouvelle issue
        serializer.save(author=self.request.user, project=project)
    
    
    def get_permissions(self):
        """
        Instancie et renvoie la liste des autorisations que cette vue nécessite.
        """
        try:
            if self.action in ['update', 'partial_update', 'destroy']:
                permission_classes = [IsIssueAuthor]
            elif self.action == 'create':
                project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
                if IsAuthorOrContributor().has_object_permission(self.request, None, project):
                    permission_classes = [permissions.AllowAny]
                else:
                    raise PermissionDenied("Vous n'êtes pas autorisé à créer un problème pour ce projet")
            else:
                permission_classes = [IsAuthorOrContributor]
        except Http404:
            raise Http404("Le projet demandé n'existe pas.")

        return [permission() for permission in permission_classes]





class CommentViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour la vue de l'API des objets 'Comment'.
    """

    # Récupérer tous les commentaires
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Cette méthode est surchargée pour personnaliser la queryset en fonction de l'utilisateur qui fait la requête.
        """

        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user

        # Renvoyer les commentaires où l'utilisateur est l'auteur ou contributeur
        return Comment.objects.filter(Q(issue__project__author=user) | Q(issue__project__contributors=user))

    def perform_create(self, serializer):
        """
        Surchargée pour ajouter l'auteur et l'issue lors de la création d'un commentaire.
        """

        # Récupérer l'ID de l'issue
        issue_id = self.kwargs['issue_pk']

        # Trouver l'issue correspondante
        issue = get_object_or_404(Issue, pk=issue_id)

        # Enregistrer le nouveau commentaire
        serializer.save(author=self.request.user, issue=issue)
        
    def get_permissions(self):
        """
        Instancie et renvoie la liste des autorisations que cette vue nécessite.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsCommentAuthor]
        elif self.action == 'create':
            issue = get_object_or_404(Issue, pk=self.kwargs['issue_pk'])
            if IsIssueAuthorOrContributor().has_object_permission(self.request, None, issue):
                permission_classes = [permissions.AllowAny]
            else:
                raise PermissionDenied("Vous n'êtes pas autorisé à créer un commentaire pour ce problème")
        else:
            permission_classes = [IsIssueAuthorOrContributor]

        return [permission() for permission in permission_classes]



class UserListView(generics.ListAPIView):
    """
    Un View générique pour lister tous les utilisateurs.
    """

    # Récupérer tous les utilisateurs
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class ProjectUserViewSet(viewsets.ViewSet):
    """
    ViewSet pour obtenir les utilisateurs liés à un projet spécifique.
    """
    # Définition de la classe de permissions
    permission_classes = [IsAuthenticated]

    def list(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)

        # Vérifiez si l'utilisateur est l'auteur du projet ou un contributeur
        if not project.author == request.user and not project.contributors.filter(id=request.user.id).exists():
            return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette ressource.")

        serializer = UserSerializer(project.contributors, many=True)
        return Response(serializer.data)
