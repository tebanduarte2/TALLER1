from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Prefetch, Q
from .models import Professor, Rating, Course, Student
from django.views.decorators.cache import cache_page


def home(request):

    return render(request, 'fourStars/home.html', {'search': 'True'})


def about(request):
    
    return render(request, 'fourStars/about.html')


def professor_rating(request, professor_id):
    professor = get_object_or_404(Professor, id=professor_id)

    # Assuming the student is already known (you can modify this depending on how you get the student)
    student = Student.objects.first()

    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')

        if rating_value:
            # Check if the student already rated this professor
            rating, created = Rating.objects.update_or_create(
                student=student,
                professor=professor,
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
        'opciones': range(1, 6)
    })

def add_professor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        selected_courses = request.POST.getlist('cursos')

        # Validate email
        if not email.endswith('@eafit.edu.co'):
            selected_courses = [int(course_id) for course_id in selected_courses]
            return render(request, 'fourStars/addProfessor.html', {
                'courses': Course.objects.all(),
                'error': 'El correo debe terminar con @eafit.edu.co',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'selected_courses': selected_courses,
            })

        # Ensure at least one course is selected
        if len(selected_courses) == 0:
            selected_courses = [int(course_id) for course_id in selected_courses]
            return render(request, 'fourStars/addProfessor.html', {
                'courses': Course.objects.all(),
                'error': 'Debe seleccionar al menos un curso.',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'selected_courses': selected_courses,
            })

        # Create the Professor instance
        professor = Professor.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # Add selected courses
        for course_id in selected_courses:
            course = Course.objects.get(id=course_id)
            professor.courses.add(course)

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

