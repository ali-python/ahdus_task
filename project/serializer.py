from rest_framework import serializers
from .models import Project, ProjectMembership, Comment
from user.serializer import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner']

class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'role']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'content', 'created_at']
