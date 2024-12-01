0#\27 from django.shortcuts import render
from functools import partial
from turtle import color
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from home.models import Person
from home.serializers import LoginSerializer, PeopleSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.core.paginator import Paginator



# Create your views here.

# @api_view(['GET', 'POST', 'PUT'])  
# def index(request):
#     courses = {
#         'course_name' : 'python',
#         'learn' : ['django', 'flask', 'Tornado', 'FastAPI'],
#         'course_provider' : 'Scalar'
#     } 
#     if request.method == 'GET':
#         print(request.GET.get('search'))
#         print("You hit a GET method")
#         return Response(courses)
#     elif request.method == 'POST':
#         data = request.data
#         print("******")
#         print(data['age'])
#         print("******")
#         print("You hit a POST method")
#         return Response(courses)
#     elif request.method == 'PUT':
#         print("You hit a PUT method")
#         return Response(courses)

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({ 'status' : False, 'message' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST )

        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'] )
        if not user:
            return Response({ 'status' : False, 'message' : 'Invalid username or password' }, status=status.HTTP_400_BAD_REQUEST )

        token, _ = Token.objects.get_or_create(user = user)
        print(token)
        return Response({ 'status' : True, 'message' : 'User Login', 'token' : str(token) }, status=status.HTTP_201_CREATED )


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response({ 'status' : True, 'message' : 'User Created' }, status=status.HTTP_201_CREATED )
        else:
            return Response({ 'status' : False, 'message' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST )

            

@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        json_response = {
            'name' : 'Scalar',
            'courses' : ['C++', 'Python'],
            'method' : 'GET'
        }
    else: 
        data = request.data
        print(data)
        json_response = {
            'name' : 'Skill Academy',
            'courses' : ['C++', 'Python', 'Full Stack Python Development'],
            'method' : 'POST'
        }
    return Response(json_response)

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        # data = serializer.validated_data
        data = serializer.data
        print(data)
        return Response({'message' : 'Login Success'})

    return Response(serializer.errors)

class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            print(request.user)
            # objs = Person.objects.filter(color__isnull = False)
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3

            paginator = Paginator(objs, page_size)

            serializer = PeopleSerializer(paginator.page(page), many = True)

            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status' : 'False',
                'message' : 'Invalid Page Number'
            })
        # print(paginator.page(page))
        # return Response({ "Message" : "This is a get request" })
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
        # return Response({ "Message" : "This is a post request" })
    
    def put(self, request):
        # try:
        #     person = Person.objects.get(pk = pk)
        # except Person.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
        # return Response({ "Message" : "This is a put request" })
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
        # return Response({ "Message" : "This is a patch request" })
   
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Person Deleted'})
        # return Response({ "Message" : "This is a delete request" })
        


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(objs, many = True)
        serializer_context = {
            "request" : (request),
        }
        context = serializer_context
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Person Deleted'})

class PeopleViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PeopleSerializer
    http_method_names = ['GET', 'POST']

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PeopleSerializer(queryset, many=True)
        return Response({ 'status' : 200, 'data' : serializer.data }, status = status.HTTP_204_NO_CONTENT)
    
    @action(detail = False, methods = ['POST'])
    def send_mail_to_person(self, request):
        return Response({
            'status' : True,
            'message' : 'email sent successfully',
        })
    
    @action(detail = True, methods = ['POST'])
    def send_mail_to_person(self, request, pk):
        print(pk)
        return Response({
            'status' : True,
            'message' : 'email sent successfully',
        })
    
    @action(detail = True, methods = ['GET'])
    def send_mail_to_person(self, request, pk):
        obj = Person.objects.get(pk = pk)
        serializer = PeopleSerializer(obj)
        return Response({
            'status' : True,
            'message' : 'email sent successfully',
            'data' : serializer.data,
        })