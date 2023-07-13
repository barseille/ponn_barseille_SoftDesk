from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur qui fait la requête est l'auteur du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
    
class IsContributor(permissions.BasePermission):
    """
    Vérifie si l'utilisateur qui fait la requête est un contributeur du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        return request.user in obj.contributors.all()

    
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

