from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('professors/', views.professors, name='professors'),
    path('professorView/<int:professor_id>/', views.professor_view, name='professor_view'),
    path('professorRating/<int:professor_id>', views.professor_rating, name='professor_rating'),
     path('addProfessor/', views.add_professor, name='add_professor'),
    ] + debug_toolbar_urls()    
       

