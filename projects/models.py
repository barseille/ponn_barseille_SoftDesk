from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    """
    Ce modèle représente un projet. Un projet a un auteur, un titre, une description, un type 
    et peut avoir plusieurs contributeurs.
    """
    
    # Champs de choix pour le type de projet
    PROJECT_TYPE_CHOICES = [('WEB', 'Web'), 
                            ('IOS', 'iOS'), 
                            ('ANDROID', 'Android')]
    
    # Clé étrangère vers le modèle utilisateur. Si l'utilisateur est supprimé, tous ses projets sont supprimés.
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authored_projects")
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=7, choices=PROJECT_TYPE_CHOICES)
    
    # Modèle "Contributor" est un modèle intermédiaire, il représente la relation "contribuer à" entre l'utilisateur et projet.
    contributors = models.ManyToManyField(get_user_model(), through='Contributor', related_name='contributed_projects')
    

class Contributor(models.Model):
    """
    Ce modèle représente un contributeur à un projet. Un contributeur est lié à un utilisateur et à un projet.
    """
    
    # Clé étrangère vers le modèle utilisateur. Si l'utilisateur est supprimé, toutes ses contributions sont supprimées.
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='contributions')
    
    # Clé étrangère vers le modèle Project. Si le projet est supprimé, toutes les contributions à ce projet sont supprimées.
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_contributors')


class Issue(models.Model):
    """
    Ce modèle représente un problème liée à un projet. Un problème a un titre, une description, une priorité,
    une étiquette (tag), un statut, un auteur et une date de création.
    """
    
    # Choix du niveau de difficulté du problème
    PRIORITY_CHOICES = [("FAIBLE", "faible"), 
                        ("MOYEN", "moyen"), 
                        ("ELEVEE", "élevée")]
    
    # Champs de choix pour l'étiquette du problème
    TAG_CHOICES = [('BUG', 'Bug'), 
                   ('AMELIORATION', 'Amélioration'), 
                   ('TACHE', 'Tâche')]
    
    # Champs de choix pour le statut du problème
    STATUS_CHOICES = [('A_FAIRE', 'A faire'), 
                      ('EN_COURS', 'En cours'), 
                      ('TERMINE', 'Terminé')]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=12, choices=TAG_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    
    # Clé étrangère vers le modèle Project. Si le projet est supprimé, toutes les problèmes liées sont supprimées.
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    
    # Clé étrangère vers le modèle utilisateur. Si l'utilisateur est supprimé, toutes ses problèmes sont supprimées.
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authored_issues")
    
    # La date et l'heure de la création du prblème
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Ce modèle représente un commentaire sur un problème. Un commentaire a une description,
    un auteur et une date de création.
    """
    description = models.TextField()
    
     # Clé étrangère vers le modèle utilisateur. Si l'utilisateur est supprimé, tous ses commentaires sont supprimés.
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="authored_comments")
    
    # Clé étrangère vers le modèle Issue. Si l'issue est supprimée, tous les commentaires liés sont supprimés.
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    
    # La date et l'heure de la création du commentaire
    created_time = models.DateTimeField(auto_now_add=True)
