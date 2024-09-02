from django.shortcuts import render
from .models import Professor
def home(request):
    return render(request, 'fourStars/home.html')

def about(request):
    return render(request, 'fourStars/about.html')

def professors(request):
    professors = Professor.objects.all()
    return render(request, 'fourStars/professors.html', {'professors': professors})
