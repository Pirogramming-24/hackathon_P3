from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('<int:session_id>/add/', views.add_question, name='add_question'),
    path('<int:question_id>/reply/', views.add_reply, name='add_reply'),
    path('<int:question_id>/toggle/', views.toggle_answered, name='toggle_answered'),
]