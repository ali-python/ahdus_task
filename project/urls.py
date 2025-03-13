from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename="project")
router.register(r'comments', CommentViewSet, basename="comment")

urlpatterns = [
    path('', include(router.urls)),
]
