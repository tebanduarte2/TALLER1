from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class StudentFactory:
    @staticmethod
    def create(first_name, last_name, email, password, **extra_fields):
        if not email.endswith('@eafit.edu.co'):
            raise ValidationError("El correo debe terminar con @eafit.edu.co")

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields
        )
        return user
