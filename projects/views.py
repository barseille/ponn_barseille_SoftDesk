from rest_framework import viewsets, generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour la vue de l'API des objets 'Project'.
    """
    
    # Récupérer tous les projets
    queryset = Project.objects.all()
    
    # Utilisation du serializer au projet
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        Cette méthode est surchargée pour personnaliser la queryset 
        en fonction de l'utilisateur qui fait la requête.
        """
        
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        
        # Renvoyer les projets où l'utilisateur est l'auteur ou contributeur
        # On garantit que chaque instance de projet dans queryset est unique avec la méthode distinct().
        return Project.objects.filter(Q(author=user) | Q(contributors=user)).distinct()


    def perform_create(self, serializer):
        """
        Surchargée pour ajouter l'auteur lors de la création d'un projet.
        """
        
        # Définir l'auteur du projet lors de sa création
        serializer.save(author=self.request.user)


    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        """
        Méthode personnalisée pour ajouter un contributeur à un projet.
        """
        
        # Récupérer le projet actuel
        project = self.get_object()
        
        # Récupérer l'utilisateur qui doit être ajouté en tant que contributeur
        contributor_user = get_user_model().objects.get(id=request.data.get('contributor_id'))
        
        # Vérifier si l'utilisateur est déjà contributeur du projet
        if project.contributors.filter(id=contributor_user.id).exists():
            
            # Si oui, renvoyer un message d'erreur
            return Response({'message': 'Cet utilisateur est déjà un contributeur du projet.'})
        
        # Si non, créer un nouvel enregistrement dans la table des contributeurs
        contributor = Contributor.objects.create(user=contributor_user, project=project)
        
        return Response({'message': 'Contributeur ajouté avec succès au projet.'})


    @action(detail=True, methods=['delete'], url_path='contributors/(?P<contributor_id>[^/.]+)')
    def remove_contributor(self, request, pk=None, contributor_id=None):
        """
        Méthode personnalisée pour supprimer un contributeur d'un projet.
        """
        # Récupérer le projet actuel
        project = self.get_object()
        
        try:
            # Essayer de trouver le contributeur dans le projet
            contributor = project.project_contributors.get(user_id=contributor_id)
            
        except Contributor.DoesNotExist:
            
            # Si le contributeur n'existe pas, renvoyer une erreur 404
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Si le contributeur existe, le supprimer
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class IssueViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet pour la vue de l'API des objets 'Issue'.
    """
    
    # Récupérer tous les problèmes
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

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


class UserListView(generics.ListAPIView):
    """
    Un View générique pour lister tous les utilisateurs.
    """
    
    # Récupérer tous les utilisateurs
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
