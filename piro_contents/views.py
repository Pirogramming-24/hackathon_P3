from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from piro_sessions.models import Session
from .models import Content, ProgressBox, ProgressCheck
import uuid

# Create your views here.
def get_or_create_user_id(request):
    """사용자 ID 생성/조회"""
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id

@require_http_methods(["POST"])
def add_content(request, session_id):
    """콘텐츠 추가"""
    try:
        session = Session.objects.get(id=session_id)
    except Session.DoesNotExist:
        return redirect('/')
    
    content_text = request.POST.get('content')
    file = request.FILES.get('file')
    is_progress = request.POST.get('is_progress')
    
    if is_progress:
        # 진도 박스 생성 (기존 것 삭제)
        session.progress_boxes.all().delete()
        ProgressBox.objects.create(
            session=session,
            content=content_text,
            order=0
        )
    else:
        # 일반 콘텐츠 생성
        content_type = 'text'
        if file:
            content_type = 'image' if file.content_type.startswith('image/') else 'file'
        
        Content.objects.create(
            session=session,
            content_type=content_type,
            content=content_text,
            file=file
        )
    
    return redirect(f'/sessioner/{session_id}/?tab=contents')

@require_http_methods(["POST"])
def add_progress_check(request, box_id):
    """진도 체크 추가/수정"""
    try:
        box = ProgressBox.objects.get(id=box_id)
    except ProgressBox.DoesNotExist:
        return JsonResponse({'success': False, 'error': '진도 박스를 찾을 수 없습니다.'})
    
    user_id = get_or_create_user_id(request)
    emotion = request.POST.get('emotion')
    
    check, created = ProgressCheck.objects.update_or_create(
        progress_box=box,
        user_id=user_id,
        defaults={'emotion': emotion}
    )
    
    response = JsonResponse({
        'success': True,
        'stats': box.get_stats(),
        'emotion': emotion
    })
    response.set_cookie('user_id', user_id, max_age=365*24*60*60)
    return response