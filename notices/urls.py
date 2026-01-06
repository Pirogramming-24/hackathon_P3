from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
    path('<int:session_id>/add/', views.add_notice, name='add_notice'),
]