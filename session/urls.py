from django.urls import path
from . import views

urlpatterns = [
    path('session-admin/', views.session_admin, name='session_admin'),
]
