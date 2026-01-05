from django.shortcuts import render

# Create your views here.
def qna_admin(request):
    week = request.GET.get('week')
    day = request.GET.get('day')
    time = request.GET.get('time')

    return render(request, 'qna_admin.html', {
        'week': week,
        'day': day,
        'time': time,
    })

def qna_user(request):
    return render(request, 'qna_user.html')