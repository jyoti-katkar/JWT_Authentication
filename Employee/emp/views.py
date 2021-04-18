from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import employees
from .serializer import employeesSerializer
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

# Create your views here.
from rest_framework.views import APIView


def homepage (request):
    return render(request, 'Home.html')


# generate token by verifying user cradentials
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login (request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class employeeList(APIView):
    # get fun to read data
    permission_classes = (IsAuthenticated,)

    def get (self, request):
        emp = employees.objects.all()
        serializer = employeesSerializer(emp, many=True)
        return Response({'data':serializer.data})

    def post(self, request, format=None):
        serializer = employeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class employeeDetail(APIView):
    """
            Retrieve, update or delete a snippet instance.
            """
    permission_classes = (IsAuthenticated,)

    def get_object (self, pk):
        try:
            return employees.objects.get(pk=pk)
        except employees.DoesNotExist:
            raise Http404

    def get (self, request, pk, format=None):
        emp = self.get_object(pk)
        serializer = employeesSerializer(emp)
        return Response(serializer.data)

    def put (self, request, pk, format=None):
        emp = self.get_object(pk)
        serializer = employeesSerializer(emp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete (self, request, pk, format=None):
        emp = self.get_object(pk)
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


