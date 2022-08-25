from django.db import models
from django.contrib.auth.models import User

# Create your models here.

Category_choices = (
    ('Political Science','Political Science'),
    ('Sociology', 'Sociology'),
    ('Socialwork','Social Work'),
    ('Health and Body','Health and Body'),
    ('Computer Science','Computer Science'),
    ('Information Technology','Information Technology'),
    ('Managerial Studies','Managemerial Studies'),
    ('Accountancy','Accountancy'),
    ('Economics','Economics'),
    ('English Literature','English Literature'),
    ('English Grammar','English Grammar'),
    ('Maths','Maths'),
    ('Chemistry','Chemistry'),
    ('Biology','Biology'),
    ('Geology','Geology'),
    ('Physics','Physics'),
    ('Astronomy','Astronomy'),
    ('Architectural and Structural',"Architectural and Sructural"),
    ('Food and Hospitality','Food and Hospitality'),
)

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name ='notes'
        verbose_name_plural= 'notes'
    
    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class stNotes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=Category_choices, default='Information Technology')
    title = models.CharField(max_length=200)
    description = models.TextField()
    files = models.FileField(upload_to="fileuploads",null=True, blank=True )
    

    def __str__(self):
        return self.category

class Todo(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   title = models.CharField(max_length=100)
   is_finished = models.BooleanField(default=False)

   def __str__(self):
        return self.title

class notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
        
    def __str__(self):
        return self.title

class Helppost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
