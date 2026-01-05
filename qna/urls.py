from django.urls import path
from . import views

urlpatterns = [
    path('qna/admin/', views.qna_admin, name='qna_admin'),
    path('qna/user/', views.qna_user, name='qna_user'),
]
