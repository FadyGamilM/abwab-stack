from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from employee.models import Employee

# Create your views here.


from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def student_index(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_serializers = StudentSerializer(students, many=True)
        return Response(student_serializers.data)
    elif request.method == 'POST':
        student_serializers = StudentSerializer(data=request.data)
        if student_serializers.is_valid():
            student_serializers.save()
            return Response(student_serializers.data, status=status.HTTP_201_CREATED)
        return Response(student_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def student_by_id(request, id):
    try:
        # we try to get the student first in-case we are going to update or delete it
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        student_serializers = StudentSerializer(student)
        return Response(student_serializers.data)

    elif request.method == 'PUT':
        student_serializers = StudentSerializer(student, data=request.data)

        if student_serializers.is_valid():
            student_serializers.save()
            return Response(student_serializers.data)

        return Response(student_serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        student_serializers = StudentSerializer(
            student, data=request.data, partial=True)

        if student_serializers.is_valid():
            student_serializers.save()
            return Response(student_serializers.data)

        return Response(student_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class Employees(APIView):
    def get(self, request):
        emps = Employee.objects.all()
        emp_serializer = EmployeeSerializer(emps, many=True)
        return Response(emp_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        emp_serializer = EmployeeSerializer(data=request.data)
        if emp_serializer.is_valid():
            emp_serializer.save()
            return Response(emp_serializer.data, status=status.HTTP_201_CREATED)
        return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetails(APIView):
    def get_object(self, id):
        try:
            return Employee.objects.get(pk=id)
        except Employee.DoesNotExist:
            return None

    def get(self, request, id):
        emp = self.get_object(id)
        if emp is not None:
            emp_serializer = EmployeeSerializer(emp)
            return Response(emp_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        emp = self.get_object(id)
        if emp is not None:
            emp_serializer = EmployeeSerializer(emp, data=request.data)
            if emp_serializer.is_valid():
                emp_serializer.save()
                return Response(emp_serializer.data, status=status.HTTP_200_OK)
            return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        emp = self.get_object(id)
        if emp is not None:
            emp.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
