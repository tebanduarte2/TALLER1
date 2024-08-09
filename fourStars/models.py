from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Student(AbstractUser):
   # abstractuser is a built-in model that comes with django that we can use to create a user model with a username, email, first name, last name, etc.
   #this is usefull because we can use the built-in authentication system that django provides
   pass

class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    professors = models.ManyToManyField('Professor', related_name='courses')

class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    
    
 
  

class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()