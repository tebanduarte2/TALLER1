from django.db import models 





# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=50)
    
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
            return "{:.1f}".format(sum(rating.rating for rating in ratings) / ratings.count())
        return None
    #method for formating decimal to 2 decimal places
    
    
    


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Ensures ratings are deleted when a student is deleted
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='ratings')  # Ensures ratings are deleted when a professor is deleted
    rating = models.IntegerField()
    review = models.TextField()

    class Meta:
        unique_together = ('student', 'professor')
        
    def __str__(self):  
        return str(self.rating)

    
        
           
    
    
    


    
    
