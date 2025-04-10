from django.core.management.base import BaseCommand
from fourStars.models import Course, Professor


class Command(BaseCommand):
    help = 'Seeds the database with sample courses and professors'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        # Creamos algunos profesores
        prof1, _ = Professor.objects.get_or_create(
            email='john.doe@example.com',
            defaults={'first_name': 'John', 'last_name': 'Doe'}
        )
        prof2, _ = Professor.objects.get_or_create(
            email='jane.smith@example.com',
            defaults={'first_name': 'Jane', 'last_name': 'Smith'}
        )

        # Creamos cursos y les asignamos profesores
        course_data = [
            {'name': 'Matemáticas I', 'code': 'MATH101', 'professors': [prof1]},
            {'name': 'Física I', 'code': 'PHYS101', 'professors': [prof2]},
            {'name': 'Programación', 'code': 'CS101', 'professors': [prof1, prof2]},
        ]

        for data in course_data:
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults={'name': data['name']}
            )
            if created:
                course.professors.set(data['professors'])  # asignamos profesores
                course.save()
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Course already exists: {course.name}'))

        self.stdout.write(self.style.SUCCESS('Done seeding.'))
