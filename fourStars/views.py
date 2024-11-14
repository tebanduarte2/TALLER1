from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Prefetch, Q
from .models import Professor, Rating, Course
from django.views.decorators.cache import cache_page
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import StudentLoginForm, StudentRegistrationForm
from django.contrib.auth.decorators import login_required


def home(request):

    return render(request, 'fourStars/home.html', {'search': 'True'})


def about(request):
    
    return render(request, 'fourStars/about.html')


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            messages.success(request, f'Welcome {user.first_name}, your account has been created!')
            return redirect('home')  # Redirect to home page or wherever you want
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'fourStars/register.html', {'form': form})

class StudentLoginView(LoginView):
    form_class = StudentLoginForm
    template_name = 'fourStars/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"Welcome back, {user.first_name}!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')  # Ensure this redirects to 'home'

    
        

class StudentLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # Redirect to the homepage after logout


@login_required  # Ensure that only logged-in users can access this view
def professor_rating(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)

    # Get the currently logged-in student from the request
    student = request.user

    if request.method == 'POST':
        course_id = request.POST.get('course')
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')

        # Validate course selection
        if not course_id:
            error = "Debe seleccionar una materia"
            return render(request, 'fourStars/professorRating.html', {
                'professor': professor,
                'opciones': range(1, 6),
                'error': error,
            })

        # Ensure the selected course is taught by the professor
        course = get_object_or_404(Course, id=course_id)
        if course not in professor.courses.all():
            error = "La materia seleccionada no es impartida por este profesor."
            return render(request, 'fourStars/professorRating.html', {
                'professor': professor,
                'opciones': range(1, 6),
                'error': error,
            })

        if rating_value:
            # Check if the student already rated this professor and course
            rating, created = Rating.objects.update_or_create(
                student=student,
                professor=professor,
                course=course,
                defaults={
                    'rating': rating_value,
                    'review': review_text,
                }
            )

            # Redirect to the professor view or a success page
            return redirect('professor_view', professor_id=professor.id)
        else:
            # Return the form with an error if no rating was provided
            error = "Debe seleccionar una calificación"
            return render(request, 'fourStars/professorRating.html', {
                'professor': professor,
                'opciones': range(1, 6),
                'error': error,
            })

    # If GET request, show the form
    return render(request, 'fourStars/professorRating.html', {
        'professor': professor,
        'opciones': range(1, 6),
        'student_name': student.first_name,  # Pass student's first name to the template
    })

@login_required
def add_professor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # Get selected courses as a list 
        selected_courses = request.POST.getlist('courses')
            
        
        
        

        # Validate email
        if not email.endswith('@eafit.edu.co'):
            return render(request, 'fourStars/addProfessor.html', {
                'courses': Course.objects.all(),
                'error_message': 'El correo debe terminar con @eafit.edu.co',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })

        # Ensure at least one course is selected
        if not selected_courses:
            return render(request, 'fourStars/addProfessor.html', {
                'courses': Course.objects.all(),
                'error_message': 'Debe seleccionar al menos un curso.',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })

        # Create the Professor instance
        professor = Professor.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # Add selected courses
        for course_id in selected_courses:
            try:
                course = Course.objects.get(id=course_id)
                professor.courses.add(course)
            except Course.DoesNotExist:
                continue

        # Redirect to a success page or the homepage
        return redirect('professors')

    # If GET request, show the form
    courses = Course.objects.all()
    return render(request, 'fourStars/addProfessor.html', {'courses': courses})



def professors(request):
    search_query = request.GET.get('search', '')
    # Prefetch related ratings and courses to avoid multiple queries in the template
    professors = Professor.objects.prefetch_related('ratings', 'courses').all()
    
    if search_query:
        professors = professors.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(courses__name__icontains=search_query)
        ).distinct()
    
    professors_with_data = []
    for professor in professors:
        professors_with_data.append({
            'professor': professor,
            'average_rating': professor.average_rating,
            'ratings_count': professor.ratings.count(),
            'courses': professor.courses.all(),
        })

    return render(request, 'fourStars/professors.html', {'professors': professors_with_data, 'search_query': search_query})



 
def professor_view(request, professor_id=None):
    # Fetch professor with related courses and ratings in a single query
    professor = Professor.objects.prefetch_related(
        Prefetch('ratings', queryset=Rating.objects.select_related('student')),
        'courses'
    ).get(id=professor_id)


    rating_distribution = (
        professor.ratings.values('rating')
        .annotate(count=Count('rating'))
        .order_by('-rating')
    )
    total_ratings = sum(item['count'] for item in rating_distribution) or 1

    # Calculate the distribution and percentage of each rating
    ratings_distribution = [
        {
            'stars': i,
            'percentage': next(
                (
                    (item['count'] / total_ratings) * 100
                    for item in rating_distribution
                    if item['rating'] == i
                ),
                0,
            ),
            'count': next(
                (item['count'] for item in rating_distribution if item['rating'] == i),
                0,
            ),
        }
        for i in range(5, 0, -1)
    ]


    # Ratings are already prefetched, so no additional queries needed
    ratings = professor.ratings.all()
    ratings_count = len(ratings)

    # Prepare the context with prefetched courses
    context = {
        'professor': professor,
        'ratings_distribution': ratings_distribution,
        'ratings': ratings,
        'ratings_count': ratings_count,
        'courses': professor.courses.all(),
    }

    return render(request, 'fourStars/professorView.html', context)

