from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogManagementViewSet
from . import views

router = DefaultRouter()
router.register(r'logs', LogManagementViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
    path('app/', views.log_management, name='log_management'),
]