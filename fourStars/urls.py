from django.urls import path
from django.contrib.auth import views as auth_views
from debug_toolbar.toolbar import debug_toolbar_urls

from .views import (
    HomeView, AboutView, RegisterView,
    StudentLoginView, StudentLogoutView,
    ProfessorListView, ProfessorDetailView,
    ProfessorRatingView, AddProfessorView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('professors/', ProfessorListView.as_view(), name='professors'),
    path('professorView/<int:professor_id>/', ProfessorDetailView.as_view(), name='professor_view'),
    path('professorRating/<int:professor_id>/', ProfessorRatingView.as_view(), name='professor_rating'),
    path('addProfessor/', AddProfessorView.as_view(), name='add_professor'),
    path('login/', StudentLoginView.as_view(template_name='fourStars/login.html'), name='login'),
    path('logout/', StudentLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
] + debug_toolbar_urls()