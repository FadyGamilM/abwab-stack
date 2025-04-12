from django.urls import path
from . import views

urlpatterns = [
    path('students', views.student_index, name='students-index'),
    path('students/<int:id>', views.student_by_id, name='student_by_id'),

    path('employees', views.Employees.as_view(), name='employees'),
    path('employees/<int:id>', views.EmployeeDetails.as_view(),
         name='employee_by_id'),

    path('companies', views.Companies.as_view(), name='companies'),
    path('companies/<int:pk>', views.CompanyDetails.as_view(), name='company_by_id'),

]
