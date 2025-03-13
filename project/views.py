from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, ProjectMembership, Comment
from .serializer import ProjectSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from user.models import *
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Q


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "add_member":
            return Project.objects.filter(
                projectmembership__user=self.request.user, 
                projectmembership__role="owner"
            )

        return Project.objects.filter(
            Q(members=self.request.user) | Q(owner=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMembership.objects.create(user=self.request.user, project=project, role='owner')

    @action(detail=True, methods=['POST'])
    def add_member(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound("Project not found.")

        is_owner = ProjectMembership.objects.filter(user=request.user, project=project, role='owner').exists()
        if not is_owner:
            raise PermissionDenied("Only the project owner can add members.")

        user_id = request.data.get('user_id')
        role = request.data.get('role', 'reader')

        if not user_id:
            return Response({"error": "User ID is required"}, status=400)

        allowed_roles = ['owner', 'editor', 'reader', 'none']
        if role not in allowed_roles:
            return Response({"error": f"Invalid role: {role}. Allowed roles: {allowed_roles}"}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")

        if user == request.user:
            return Response({"error": "You are already the project owner."}, status=400)

        if ProjectMembership.objects.filter(user=user, project=project).exists():
            return Response({"error": "User is already a member of this project."}, status=400)

        ProjectMembership.objects.create(user=user, project=project, role=role)

        return Response({"message": f"Member '{user.email}' added successfully as '{role}'."}, status=201)

    def destroy(self, request, *args, **kwargs):
        project_id = kwargs.get("pk")
        project = self.get_queryset().filter(id=project_id).first()
        if not project:
            raise NotFound("Project not found.")

        if project.owner != request.user:
            raise PermissionDenied("Only the project owner can delete this project.")

        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(project__members=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        membership = ProjectMembership.objects.filter(user=self.request.user, project=project).first()

        if not membership or membership.role not in ['owner', 'editor']:
            raise PermissionDenied("You do not have permission to comment") 
        serializer.save(user=self.request.user)