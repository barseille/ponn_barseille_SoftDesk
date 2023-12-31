from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAuthor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur qui fait la requête est l'auteur du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        else:
            raise PermissionDenied("Vous n'êtes pas autorisé, vous n'êtes pas l'auteur de ce projet")
    
class IsContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur qui fait la requête est un contributeur du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user=request.user).exists()


    
class IsIssueAuthor(permissions.BasePermission):
    """
   Vérifie si l'utilisateur qui fait la requête est l'auteur du problème.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    
class IsCommentAuthor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur qui fait la requête est l'auteur du commentaire.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur qui fait la requête est l'auteur ou un contributeur du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        is_author_or_contributor = request.user == obj.author or obj.project_contributors.filter(user=request.user).exists()
        if not is_author_or_contributor:
            raise PermissionDenied("Vous n'êtes pas autorisé à créer un problème pour ce projet")
        return is_author_or_contributor


class IsIssueAuthorOrContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur qui fait la requête est l'auteur ou un contributeur du problème.
    """
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or obj.project.project_contributors.filter(user=request.user).exists()


