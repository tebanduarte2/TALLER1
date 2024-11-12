from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError



class StudentManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class Student(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # add today as default
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = StudentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50, unique=True)
    professors = models.ManyToManyField('Professor', related_name='courses')

    def __str__(self):
        return self.name  

class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    

    def __str__(self):
        return self.first_name + ' ' + self.last_name 
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            # Calculate the average rating for the professor, and format it to 2 decimal places
            return float("{:.1f}".format(sum(rating.rating for rating in ratings) / ratings.count()))
        return None
    #method for formating decimal to 2 decimal places
    
    
    


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Ensures ratings are deleted when a student is deleted
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='ratings')  # Ensures ratings are deleted when a professor is deleted
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)  # Ensures ratings are linked to a course
    rating = models.IntegerField()
    review = models.TextField()

    class Meta:
        unique_together = ('student', 'professor', 'course')  # Ensure a student can only rate a professor for a specific course once

    def clean(self):
        # Ensure the course is taught by the professor
        if not self.professor.courses.filter(id=self.course.id).exists():
            raise ValidationError(f"The course '{self.course}' is not taught by Professor {self.professor}.")

    def save(self, *args, **kwargs):
        # Call clean method before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):  
        return f"{self.student} rated {self.professor} for {self.course}: {self.rating}"


    
        
           
    
    
    


    
    
