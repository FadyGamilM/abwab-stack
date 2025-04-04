from django.db import models

# Create your models here.


class Employee(models.Model):
    emp_id = models.CharField()
    name = models.CharField()
    yoe = models.SmallIntegerField()


class Company(models.Model):
    company_id = models.CharField()
    name = models.CharField()
