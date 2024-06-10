from django.db import models

# Create your models here.
from django.db import models

# when this file changes, need to run
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
class Question(models.Model):
    number = models.IntegerField()
    question_text = models.TextField()
    possible_answers = models.TextField()