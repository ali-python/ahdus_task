from django.db import models
from user.models import CustomUser

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_projects")
    members = models.ManyToManyField(CustomUser, through='ProjectMembership', related_name="projects")

    def __str__(self):
        return self.name

class ProjectMembership(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('editor', 'Editor'),
        ('reader', 'Reader'),
        ('none', 'No Role')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='none')

    class Meta:
        unique_together = ('user', 'project')


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.content[:20]}"
