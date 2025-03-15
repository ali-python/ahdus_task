from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from project.models import Project, ProjectMembership


class ProjectMemberTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.owner = CustomUser.objects.create_user(email="owner@example.com", password="password", username="owner")
        self.member = CustomUser.objects.create_user(email="member@example.com", password="password", username="member")
        self.other_user = CustomUser.objects.create_user(email="other@example.com", password="password", username="other")

        self.project = Project.objects.create(name="Test Project", owner=self.owner)
        ProjectMembership.objects.create(user=self.owner, project=self.project, role="owner")

        self.add_member_url = reverse("project-add-member", kwargs={"pk": self.project.id})

        self.client.force_authenticate(user=self.owner)

    def test_owner_can_add_member(self):
        """Project owner should be able to add a member"""
        response = self.client.post(self.add_member_url, {"user_id": self.member.id, "role": "reader"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProjectMembership.objects.filter(user=self.member, project=self.project).exists())

    def test_non_owner_cannot_add_member(self):
        """A non-owner should get 404 if they cannot access the project"""
        self.client.force_authenticate(user=self.member)  
        response = self.client.post(self.add_member_url, {"user_id": self.other_user.id, "role": "reader"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 


    def test_cannot_add_same_member_twice(self):
        """Adding the same member twice should return 400"""
        ProjectMembership.objects.create(user=self.member, project=self.project, role="reader")  # Already exists
        response = self.client.post(self.add_member_url, {"user_id": self.member.id, "role": "reader"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_user_id(self):
        """Should return 400 if user_id does not exist"""
        response = self.client.post(self.add_member_url, {"user_id": 9999, "role": "reader"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_invalid_role(self):
        """Should return 400 if role is invalid"""
        response = self.client.post(self.add_member_url, {"user_id": self.member.id, "role": "invalid_role"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_cannot_add_themselves_again(self):
        """Owner should not be able to add themselves as a member"""
        response = self.client.post(self.add_member_url, {"user_id": self.owner.id, "role": "owner"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_can_access_endpoint(self):
        """Authenticated user should get a response (even if they don't have permission)"""
        response = self.client.get(self.add_member_url)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 