from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
    path('<int:session_id>/add/', views.add_notice, name='add_notice'),
    path('<int:notice_id>/edit/', views.edit_notice, name='edit_notice'),      # 추가
    path('<int:notice_id>/delete/', views.delete_notice, name='delete_notice'),  # 추가
]