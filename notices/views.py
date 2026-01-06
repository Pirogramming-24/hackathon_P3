from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from piro_sessions.models import Session
from .models import Notice

# Create your views here.
@require_http_methods(["POST"])
def add_notice(request, session_id):
    """공지사항 추가"""
    try:
        session = Session.objects.get(id=session_id)
    except Session.DoesNotExist:
        return redirect('/')
    
    title = request.POST.get('title')
    content = request.POST.get('content')
    file = request.FILES.get('file')
    
    Notice.objects.create(
        session=session,
        title=title,
        content=content,
        file=file
    )
    
    return redirect(f'/sessioner/{session_id}/?tab=notice')

# ===== 추가: 공지사항 수정 =====
@require_http_methods(["POST"])
def edit_notice(request, notice_id):
    """공지사항 수정"""
    try:
        notice = Notice.objects.get(id=notice_id)
    except Notice.DoesNotExist:
        return redirect('/')
    
    title = request.POST.get('title')
    content = request.POST.get('content')
    file = request.FILES.get('file')
    
    notice.title = title
    notice.content = content
    if file:
        notice.file = file
    notice.save()
    
    return redirect(f'/sessioner/{notice.session.id}/?tab=notice')

# ===== 추가: 공지사항 삭제 =====
@require_http_methods(["POST"])
def delete_notice(request, notice_id):
    """공지사항 삭제"""
    try:
        notice = Notice.objects.get(id=notice_id)
        session_id = notice.session.id
        notice.delete()
    except Notice.DoesNotExist:
        return redirect('/')
    
    return redirect(f'/sessioner/{session_id}/?tab=notice')