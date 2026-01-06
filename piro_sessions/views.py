from django.shortcuts import render, redirect
from .models import Session
from piro_contents.models import ProgressCheck
import uuid

# Create your views here.
def get_or_create_user_id(request):
    """사용자 ID 생성/조회"""
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id

def initial_screen(request):
    """초기 화면"""
    sessions = Session.objects.all()
    return render(request, 'piro_sessions/initial.html', {'sessions': sessions})

def participant_page(request, session_id):
    """참여자 페이지"""
    try:
        session = Session.objects.get(id=session_id)
    except Session.DoesNotExist:
        return redirect('/')
    
    user_id = get_or_create_user_id(request)
    
    # 진도 데이터 준비
    progress_data = []
    for box in session.progress_boxes.all():
        user_check = ProgressCheck.objects.filter(
            progress_box=box, user_id=user_id
        ).first()
        progress_data.append({
            'box': box,
            'stats': box.get_stats(),
            'user_emotion': user_check.emotion if user_check else None
        })
    
    context = {
        'session': session,
        'sessions': Session.objects.all(),
        'is_sessioner': False,
        'questions': session.questions.all(),
        'contents': session.contents.all(),
        'notices': session.notices.all(),
        'progress_data': progress_data,
        'current_tab': request.GET.get('tab', 'qa'),
    }
    
    response = render(request, 'piro_sessions/main.html', context)
    response.set_cookie('user_id', user_id, max_age=365*24*60*60)
    return response

def sessioner_page(request, session_id):
    """세션자 페이지"""
    try:
        session = Session.objects.get(id=session_id)
    except Session.DoesNotExist:
        return redirect('/')
    
    # 진도 데이터 준비
    progress_data = [{
        'box': box,
        'stats': box.get_stats(),
    } for box in session.progress_boxes.all()]
    
    context = {
        'session': session,
        'sessions': Session.objects.all(),
        'is_sessioner': True,
        'questions': session.questions.all(),
        'contents': session.contents.all(),
        'notices': session.notices.all(),
        'progress_data': progress_data,
        'current_tab': request.GET.get('tab', 'qa'),
    }
    
    return render(request, 'piro_sessions/main.html', context)