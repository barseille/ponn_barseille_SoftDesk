from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Contributor, Issue, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']

class ContributorSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']  

class ProjectSerializer(serializers.ModelSerializer):
    
    contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributors']  

class IssueSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'priority', 'tag', 'status', 'project', 'author', 'created_time']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
