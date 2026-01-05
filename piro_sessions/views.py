from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Session, ProgressCheck, Question, Content, Notice
from django.db.models import Count, Q

# Create your views here.
def initial_screen(request):
    """초기 화면 - 참여자/세션자 선택"""
    sessions = Session.objects.all()
    return render(request, 'piro_sessions/initial.html', {'sessions': sessions})

def participant_page(request, session_id):
    """참여자 페이지"""
    session = get_object_or_404(Session, id=session_id)
    sessions = Session.objects.all()
    
    # 진도 체크 통계
    progress_stats = ProgressCheck.objects.filter(session=session).values('emotion').annotate(count=Count('emotion'))
    stats = {item['emotion']: item['count'] for item in progress_stats}
    
    context = {
        'session': session,
        'sessions': sessions,
        'is_sessioner': False,
        'questions': session.questions.all(),
        'contents': session.contents.all(),
        'notices': session.notices.all(),
        'progress_stats': stats,
    }
    return render(request, 'piro_sessions/main.html', context)

def sessioner_page(request, session_id):
    """세션자 페이지"""
    session = get_object_or_404(Session, id=session_id)
    sessions = Session.objects.all()
    
    # 진도 체크 통계
    progress_stats = ProgressCheck.objects.filter(session=session).values('emotion').annotate(count=Count('emotion'))
    stats = {item['emotion']: item['count'] for item in progress_stats}
    
    context = {
        'session': session,
        'sessions': sessions,
        'is_sessioner': True,
        'questions': session.questions.all(),
        'contents': session.contents.all(),
        'notices': session.notices.all(),
        'progress_stats': stats,
    }
    return render(request, 'piro_sessions/main.html', context)

@require_http_methods(["POST"])
def add_progress_check(request, session_id):
    """진도 체크 추가"""
    session = get_object_or_404(Session, id=session_id)
    emotion = request.POST.get('emotion')
    
    ProgressCheck.objects.create(session=session, emotion=emotion)
    return JsonResponse({'success': True})

@require_http_methods(["POST"])
def add_question(request, session_id):
    """질문 추가"""
    session = get_object_or_404(Session, id=session_id)
    content = request.POST.get('content')
    image = request.FILES.get('image')
    
    Question.objects.create(session=session, content=content, image=image)
    return redirect('participant_page', session_id=session_id)

@require_http_methods(["POST"])
def add_reply(request, question_id):
    """질문에 답변 추가"""
    question = get_object_or_404(Question, id=question_id)
    reply = request.POST.get('reply')
    
    question.reply = reply
    question.answered = True
    question.save()
    
    return redirect('sessioner_page', session_id=question.session.id)

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
    content_type = request.POST.get('content_type', 'text')
    title = request.POST.get('title', '')
    content = request.POST.get('content')
    file = request.FILES.get('file')
    
    Content.objects.create(
        session=session,
        content_type=content_type,
        title=title,
        content=content,
        file=file
    )
    return redirect('sessioner_page', session_id=session_id)

@require_http_methods(["POST"])
def add_notice(request, session_id):
    """공지사항 추가"""
    session = get_object_or_404(Session, id=session_id)
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    Notice.objects.create(session=session, title=title, content=content)
    return redirect('sessioner_page', session_id=session_id)