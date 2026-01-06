from django.urls import path
from . import views

app_name = 'piro_sessions'

urlpatterns = [
    path('', views.initial_screen, name='initial_screen'),
    path('participant/<int:session_id>/', views.participant_page, name='participant'),
    path('sessioner/<int:session_id>/', views.sessioner_page, name='sessioner'),
]