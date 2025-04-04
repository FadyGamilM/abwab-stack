from django.db import models

# Create your models here.


class Student(models.Model):
    student_id = models.CharField()
    name = models.CharField()
    specification = models.CharField()

    def __str__(self):
        return f"{self.student_id} - {self.name}"
