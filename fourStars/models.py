from django.db import models


# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    courses = models.ManyToManyField('Course', related_name='students')
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    professors = models.ManyToManyField('Professor', related_name='courses')

    def __str__(self):
        return self.name  

class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.first_name + ' ' + self.last_name   
    
    
 
  

class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self):  
        return str(self.rating) 