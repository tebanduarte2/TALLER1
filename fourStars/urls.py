from django.urls import path
from django.contrib.auth import views as auth_views
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('professors/', views.professors, name='professors'),
    path('professorView/<int:professor_id>/', views.professor_view, name='professor_view'),
    path('professorRating/<int:professor_id>', views.professor_rating, name='professor_rating'),
     path('addProfessor/', views.add_professor, name='add_professor'),
    path('login/', auth_views.LoginView.as_view(template_name='fourStars/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
     
    ] + debug_toolbar_urls()    
       

