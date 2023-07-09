from rest_framework import viewsets, generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, UserSerializer
from django.shortcuts import get_object_or_404



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(author=user) | Q(contributors=user))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        project = self.get_object()
        contributor_user = get_user_model().objects.get(id=request.data.get('contributor_id'))
        
        if project.contributors.filter(id=contributor_user.id).exists():
            return Response({'message': 'Cet utilisateur est déjà un contributeur du projet.'})
        
        contributor = Contributor.objects.create(user=contributor_user, project=project)
        
        return Response({'message': 'Contributeur ajouté avec succès au projet.'})

    @action(detail=True, methods=['delete'], url_path='contributors/(?P<contributor_id>[^/.]+)')
    def remove_contributor(self, request, pk=None, contributor_id=None):
        project = self.get_object()
        try:
            contributor = project.project_contributors.get(user_id=contributor_id)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(Q(project__author=user) | Q(project__contributors=user))

    def perform_create(self, serializer):
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, pk=project_id)
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(Q(issue__project__author=user) | Q(issue__project__contributors=user))

    def perform_create(self, serializer):
        issue_id = self.kwargs['issue_pk']
        issue = get_object_or_404(Issue, pk=issue_id)
        serializer.save(author=self.request.user, issue=issue)

class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
