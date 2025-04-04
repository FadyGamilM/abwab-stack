from django.urls import path
from . import views

urlpatterns = [
    path('students', views.student_index, name='students-index'),
    path('students/<int:id>', views.student_by_id, name='student_by_id')
]
