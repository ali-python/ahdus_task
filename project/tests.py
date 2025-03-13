from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from project.models import Project, ProjectMembership
from user.models import CustomUser 

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
        response = self.client.post(self.add_member_url, {"user_id": self.member.id, "role": "reader"})
        self.assertEqual(response.status_code, 201)  
        self.assertTrue(ProjectMembership.objects.filter(user=self.member, project=self.project).exists())

    def test_non_owner_cannot_add_member(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.post(self.add_member_url, {"user_id": self.other_user.id, "role": "reader"})
        self.assertEqual(response.status_code, 403)  

    def test_cannot_add_same_member_twice(self):
        ProjectMembership.objects.create(user=self.member, project=self.project, role="reader")
        response = self.client.post(self.add_member_url, {"user_id": self.member.id, "role": "reader"})
        self.assertEqual(response.status_code, 400) 

    def test_invalid_user_id(self):
        response = self.client.post(self.add_member_url, {"user_id": 9999, "role": "reader"})
        self.assertEqual(response.status_code, 404)  


    def test_invalid_role(self):
        response = self.client.post(self.add_member_url, {"user_id": self.member.id, "role": "invalid_role"})
        self.assertEqual(response.status_code, 400)  

    def test_owner_cannot_add_themselves_again(self):
        response = self.client.post(self.add_member_url, {"user_id": self.owner.id, "role": "owner"})
        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_can_access_endpoint(self):
        response = self.client.get(self.add_member_url)
        self.assertNotEqual(response.status_code, 401) 
