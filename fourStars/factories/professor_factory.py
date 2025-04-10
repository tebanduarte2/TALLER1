from fourStars.models import Professor

class ProfessorFactory:
    @staticmethod
    def create(first_name, last_name, email, courses):
        if not email.endswith('@eafit.edu.co'):
            raise ValueError("El correo debe terminar con @eafit.edu.co")

        professor = Professor.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        professor.courses.set(courses)
        return professor
