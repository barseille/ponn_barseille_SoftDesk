from django.db import models
from django.contrib.auth import get_user_model

class Project(models.Model):
    PROJECT_TYPE_CHOICES = [('WEB', 'Web'), 
                            ('IOS', 'iOS'), 
                            ('ANDROID', 'Android')]
    
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authored_projects")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=7, choices=PROJECT_TYPE_CHOICES)
    contributors = models.ManyToManyField(get_user_model(), through='Contributor', related_name='contributed_projects')

class Contributor(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_contributors')

class Issue(models.Model):
    PRIORITY_CHOICES = [("FAIBLE", "faible"), 
                        ("MOYEN", "moyen"), 
                        ("ELEVEE", "élevée")]
    
    TAG_CHOICES = [('BUG', 'Bug'), 
                   ('AMELIORATION', 'Amélioration'), 
                   ('TACHE', 'Tâche')]
    
    STATUS_CHOICES = [('A_FAIRE', 'A faire'), 
                      ('EN_COURS', 'En cours'), 
                      ('TERMINE', 'Terminé')]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=12, choices=TAG_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authored_issues")
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    description = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authored_comments")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    created_time = models.DateTimeField(auto_now_add=True)
