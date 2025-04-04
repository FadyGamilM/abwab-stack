from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer
from rest_framework import status
from rest_framework.response import Response

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
