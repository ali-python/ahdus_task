from rest_framework import serializers
from .models import Project, ProjectMembership, Comment
from user.models import CustomUser
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

class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=['owner', 'editor', 'reader', 'none'], default='reader')

    def validate_user_id(self, value):
        try:
            return CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'content', 'created_at']
