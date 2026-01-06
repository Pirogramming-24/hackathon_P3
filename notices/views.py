from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
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