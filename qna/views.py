from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Question

# Create your views here.
@require_http_methods(["POST"])
def add_question(request, session_id):
    """질문 추가"""
    content = request.POST.get('content')
    image = request.FILES.get('image')
    
    Question.objects.create(
        session_id=session_id,
        content=content,
        image=image
    )
    return redirect(f'/participant/{session_id}/?tab=qa')

@require_http_methods(["POST"])
def add_reply(request, question_id):
    """답변 추가"""
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return redirect('/')
    
    reply = request.POST.get('reply')
    
    question.reply = reply
    question.answered = True
    question.save()
    
    return redirect(f'/sessioner/{question.session.id}/?tab=qa')

@require_http_methods(["POST"])
def toggle_answered(request, question_id):
    """답변 완료 토글"""
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return JsonResponse({'success': False, 'error': '질문을 찾을 수 없습니다.'})
    
    question.answered = not question.answered
    question.save()
    
    return JsonResponse({'success': True, 'answered': question.answered})