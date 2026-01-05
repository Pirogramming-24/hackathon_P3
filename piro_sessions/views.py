from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Session, ProgressCheck, ProgressCheckBox, Question, Content, Notice
from django.db.models import Count, Q
import uuid

# Create your views here.
def get_or_create_user_id(request):
    """쿠키에서 사용자 ID 가져오기 또는 생성"""
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id

def initial_screen(request):
    """초기 화면 - 참여자/세션자 선택"""
    sessions = Session.objects.all()
    return render(request, 'piro_sessions/initial.html', {'sessions': sessions})

def participant_page(request, session_id):
    """참여자 페이지"""
    session = get_object_or_404(Session, id=session_id)
    sessions = Session.objects.all()
    user_id = get_or_create_user_id(request)
    
    # 진도 체크 박스와 통계
    progress_boxes = session.progress_boxes.all()
    progress_data = []
    for box in progress_boxes:
        stats = box.get_stats()
        user_check = ProgressCheck.objects.filter(progress_box=box, user_id=user_id).first()
        progress_data.append({
            'box': box,
            'stats': stats,
            'user_emotion': user_check.emotion if user_check else None
        })
    
    # 현재 탭 가져오기 (URL 파라미터)
    current_tab = request.GET.get('tab', 'qa')
    
    context = {
        'session': session,
        'sessions': sessions,
        'is_sessioner': False,
        'questions': session.questions.all(),
        'contents': session.contents.all(),
        'notices': session.notices.all(),
        'progress_data': progress_data,
        'current_tab': current_tab,
    }
    
    response = render(request, 'piro_sessions/main.html', context)
    response.set_cookie('user_id', user_id, max_age=365*24*60*60)  # 1년
    return response

def sessioner_page(request, session_id):
    """세션자 페이지"""
    session = get_object_or_404(Session, id=session_id)
    sessions = Session.objects.all()
    
    # 진도 체크 박스와 통계
    progress_boxes = session.progress_boxes.all()
    progress_data = []
    for box in progress_boxes:
        stats = box.get_stats()
        progress_data.append({
            'box': box,
            'stats': stats,
        })
    
    # 현재 탭 가져오기 (URL 파라미터)
    current_tab = request.GET.get('tab', 'qa')
    
    context = {
        'session': session,
        'sessions': sessions,
        'is_sessioner': True,
        'questions': session.questions.all(),
        'contents': session.contents.all(),
        'notices': session.notices.all(),
        'progress_data': progress_data,
        'current_tab': current_tab,
    }
    return render(request, 'piro_sessions/main.html', context)

@require_http_methods(["POST"])
def add_progress_check(request, box_id):
    """진도 체크 추가/수정"""
    box = get_object_or_404(ProgressCheckBox, id=box_id)
    user_id = get_or_create_user_id(request)
    emotion = request.POST.get('emotion')
    
    # 기존 체크가 있으면 업데이트, 없으면 생성
    check, created = ProgressCheck.objects.update_or_create(
        progress_box=box,
        user_id=user_id,
        defaults={'emotion': emotion}
    )
    
    stats = box.get_stats()
    
    response = JsonResponse({
        'success': True,
        'stats': stats,
        'emotion': emotion
    })
    response.set_cookie('user_id', user_id, max_age=365*24*60*60)
    return response

@require_http_methods(["POST"])
def add_question(request, session_id):
    """질문 추가"""
    session = get_object_or_404(Session, id=session_id)
    content = request.POST.get('content')
    image = request.FILES.get('image')
    
    Question.objects.create(session=session, content=content, image=image)
    return redirect(f'/participant/{session_id}/?tab=qa')

@require_http_methods(["POST"])
def add_reply(request, question_id):
    """질문에 답변 추가"""
    question = get_object_or_404(Question, id=question_id)
    reply = request.POST.get('reply')
    
    question.reply = reply
    question.answered = True
    question.save()
    
    return redirect(f'/sessioner/{question.session.id}/?tab=qa')

@require_http_methods(["POST"])
def toggle_answered(request, question_id):
    """질문 답변 완료 토글"""
    question = get_object_or_404(Question, id=question_id)
    question.answered = not question.answered
    question.save()
    
    return JsonResponse({'success': True, 'answered': question.answered})

@require_http_methods(["POST"])
def add_content(request, session_id):
    """콘텐츠 추가"""
    session = get_object_or_404(Session, id=session_id)
    content_text = request.POST.get('content')
    file = request.FILES.get('file')
    is_progress = request.POST.get('is_progress')
    
    # 진도 체크박스 생성/업데이트
    if is_progress:
        # 기존 진도 박스들 모두 삭제 (기존 체크들도 함께 삭제됨)
        session.progress_boxes.all().delete()
        
        # 새 진도 박스 생성
        ProgressCheckBox.objects.create(
            session=session,
            content=content_text,
            order=0
        )
    else:
        # 파일이 있으면 파일 타입 결정
        content_type = 'text'
        if file:
            if file.content_type.startswith('image/'):
                content_type = 'image'
            else:
                content_type = 'file'
        
        # 일반 콘텐츠 생성
        Content.objects.create(
            session=session,
            content_type=content_type,
            title='',
            content=content_text,
            file=file
        )
    
    return redirect(f'/sessioner/{session_id}/?tab=contents')

@require_http_methods(["POST"])
def add_notice(request, session_id):
    """공지사항 추가"""
    session = get_object_or_404(Session, id=session_id)
    title = request.POST.get('title')
    content = request.POST.get('content')
    file = request.FILES.get('file')
    
    # 공지사항 생성
    Notice.objects.create(
        session=session, 
        title=title, 
        content=content,
        file=file
    )
    
    return redirect(f'/sessioner/{session_id}/?tab=notice')