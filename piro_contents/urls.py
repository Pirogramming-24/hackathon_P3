from django.urls import path
from . import views

app_name = 'piro_contents'

urlpatterns = [
    path('<int:session_id>/add/', views.add_content, name='add_content'),
    path('progress/<int:box_id>/add/', views.add_progress_check, name='add_progress_check'),
]