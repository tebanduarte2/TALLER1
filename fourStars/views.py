from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Prefetch, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .factories.student_factory import StudentFactory
from .factories.professor_factory import ProfessorFactory
from django.core.exceptions import ValidationError

from .models import Professor, Rating, Course
from .forms import StudentLoginForm, StudentRegistrationForm


class HomeView(TemplateView):
    template_name = 'fourStars/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = True
        return context


class AboutView(TemplateView):
    template_name = 'fourStars/about.html'


class RegisterView(FormView):
    template_name = 'fourStars/register.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            user = StudentFactory.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password1']
            )
            login(self.request, user)
            messages.success(self.request, f'Bienvenido {user.first_name}, tu cuenta ha sido creada.')
        except ValidationError as e:
            form.add_error('email', e.message)
            return self.form_invalid(form)

        return super().form_valid(form)


class StudentLoginView(LoginView):
    form_class = StudentLoginForm
    template_name = 'fourStars/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"¡Bienvenido de nuevo, {user.first_name}!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class StudentLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class ProfessorListView(ListView):
    model = Professor
    template_name = 'fourStars/professors.html'
    context_object_name = 'professors'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = Professor.objects.prefetch_related('ratings', 'courses').all()

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(courses__name__icontains=search_query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['professors'] = [
            {
                'professor': p,
                'average_rating': p.average_rating,
                'ratings_count': p.ratings.count(),
                'courses': p.courses.all(),
            }
            for p in context['professors']
        ]
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ProfessorDetailView(DetailView):
    model = Professor
    template_name = 'fourStars/professorView.html'
    context_object_name = 'professor'
    pk_url_kwarg = 'professor_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        professor = self.object

        rating_distribution = (
            professor.ratings.values('rating')
            .annotate(count=Count('rating'))
            .order_by('-rating')
        )
        total_ratings = sum(item['count'] for item in rating_distribution) or 1

        context['ratings_distribution'] = [
            {
                'stars': i,
                'percentage': next((item['count'] / total_ratings * 100 for item in rating_distribution if item['rating'] == i), 0),
                'count': next((item['count'] for item in rating_distribution if item['rating'] == i), 0),
            }
            for i in range(5, 0, -1)
        ]
        context['ratings'] = professor.ratings.select_related('student').all()
        context['ratings_count'] = professor.ratings.count()
        context['courses'] = professor.courses.all()
        return context



class AddProfessorView(LoginRequiredMixin, View):
    template_name = 'fourStars/addProfessor.html'

    def get(self, request):
        return render(request, self.template_name, {
            'courses': Course.objects.all()
        })

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        selected_courses = request.POST.getlist('cursos')
        selected_courses_obj = Course.objects.filter(id__in=selected_courses)

        try:
            professor = ProfessorFactory.create(first_name, last_name, email, selected_courses_obj)
        except ValueError as e:
            return render(request, self.template_name, {
                'courses': Course.objects.all(),
                'error': str(e),
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'selected_courses': selected_courses_obj,
            })
        except Exception:
            return render(request, self.template_name, {
                'courses': Course.objects.all(),
                'error': 'Error al crear el profesor. Verifica que el correo sea único.',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'selected_courses': selected_courses_obj,
            })
        return redirect('professors')


class ProfessorRatingView(LoginRequiredMixin, View):
    template_name = 'fourStars/professorRating.html'

    def get(self, request, professor_id):
        professor = get_object_or_404(Professor, id=professor_id)
        return render(request, self.template_name, {
            'professor': professor,
            'opciones': range(1, 6),
            'student_name': request.user.first_name,
        })

    def post(self, request, professor_id):
        professor = get_object_or_404(Professor, id=professor_id)
        student = request.user
        course_id = request.POST.get('course')
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')

        if not course_id:
            return render(request, self.template_name, {
                'professor': professor,
                'opciones': range(1, 6),
                'error': "Debe seleccionar una materia",
            })

        course = get_object_or_404(Course, id=course_id)
        if course not in professor.courses.all():
            return render(request, self.template_name, {
                'professor': professor,
                'opciones': range(1, 6),
                'error': "La materia seleccionada no es impartida por este profesor.",
            })

        if not rating_value:
            return render(request, self.template_name, {
                'professor': professor,
                'opciones': range(1, 6),
                'error': "Debe seleccionar una calificación",
            })

        Rating.objects.update_or_create(
            student=student,
            professor=professor,
            course=course,
            defaults={
                'rating': rating_value,
                'review': review_text,
            }
        )
        return redirect('professor_view', professor_id=professor.id)