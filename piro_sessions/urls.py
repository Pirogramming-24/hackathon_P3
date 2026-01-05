from django.urls import path
from . import views

urlpatterns = [
    path('', views.initial_screen, name='initial_screen'),
    path('participant/<int:session_id>/', views.participant_page, name='participant_page'),
    path('sessioner/<int:session_id>/', views.sessioner_page, name='sessioner_page'),
    
    # AJAX/POST 요청
    path('progress-check/<int:box_id>/add/', views.add_progress_check, name='add_progress_check'),
    path('question/<int:session_id>/add/', views.add_question, name='add_question'),
    path('question/<int:question_id>/reply/', views.add_reply, name='add_reply'),
    path('question/<int:question_id>/toggle/', views.toggle_answered, name='toggle_answered'),
    path('content/<int:session_id>/add/', views.add_content, name='add_content'),
    path('notice/<int:session_id>/add/', views.add_notice, name='add_notice'),
]