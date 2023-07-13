from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Contributor, Issue, Comment


class UserSerializer(serializers.ModelSerializer):
    """
    Ce sérialiseur est utilisé pour convertir les objets User en format JSON.
    """
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class ContributorSerializer(serializers.ModelSerializer):
    """
    Ce sérialiseur est utilisé pour convertir les objets Contributor en format JSON.
    """
    
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']  


class ProjectSerializer(serializers.ModelSerializer):
    """
    Ce sérialiseur est utilisé pour convertir les objets Project en format JSON.
    """
    
    # Pour le champ 'contributors', utilise un champ lié à la clé primaire.
    contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'contributors']  


class IssueSerializer(serializers.ModelSerializer):
    """
    Ce sérialiseur est utilisé pour convertir les objets Issue en format JSON.
    """
    
    author = UserSerializer(read_only=True)
    
    # Utilise un champ lié à la clé primaire pour le champ 'project'.
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'priority', 'tag', 'status', 'project', 'author', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    """
    Ce sérialiseur est utilisé pour convertir les objets Comment en format JSON.
    """
    
    author = UserSerializer(read_only=True)
    
    # Utilise un champ lié à la clé primaire pour le champ 'issue'.
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
