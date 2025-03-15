from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, ProjectMembership, Comment
from .serializer import ProjectSerializer, CommentSerializer, AddMemberSerializer
from rest_framework.permissions import IsAuthenticated
from user.models import *
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
import logging
logger = logging.getLogger('project')

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            Q(members=self.request.user) | Q(owner=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMembership.objects.create(user=self.request.user, project=project, role='owner')
        logger.info(f"Project '{project.name}' created by {self.request.user.email}")

    @action(detail=True, methods=['POST'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied("Only the project owner can add members.")

        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data["user_id"]
        role = serializer.validated_data["role"]

        if ProjectMembership.objects.filter(user=user, project=project).exists():
            return Response({"error": "User is already a member of this project."}, status=status.HTTP_400_BAD_REQUEST)

        ProjectMembership.objects.create(user=user, project=project, role=role)
        logger.info(f"User '{user.email}' added to project '{project.name}' as '{role}'")

        return Response({"message": f"Member '{user.email}' added successfully as '{role}'."}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied("Only the project owner can delete this project.")

        logger.info(f"Project '{project.name}' deleted by {request.user.email}")
        return super().destroy(request, *args, **kwargs)
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(project__members=self.request.user).distinct()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        
        if not ProjectMembership.objects.filter(user=self.request.user, role__in=["owner", "editor"]).exists():
            logger.warning(f"User {self.request.user.id} tried to comment without permission.")
            raise PermissionDenied("You do not have permission to comment.")
        
        serializer.save(user=self.request.user)
