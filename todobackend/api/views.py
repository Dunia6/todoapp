from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodotoggleCompleteSerializer
from todo.models import Todo

from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class TodoListCreate(generics.ListCreateAPIView):
    # ListAPIView needs two attributes, serializer_class and queryset
    # We specify TodoSerializer which we earlier implemented
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user =  self.request.user
        return Todo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        # Serializer holds a django model
        serializer.save(user=self.request.user)



class TodoRetrieveUpdateDetroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # can only update, delete own posts
        return Todo.objects.filter(user=user)



class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodotoggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_update(self, serializer):
        serializer.instance.completed=not(serializer.instance.completed)
        serializer.save()



# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         try:
#             data = JSONParser().parse(request) # Ceci contient un dictionnaire
#             user = User.objects.create_user(
#                 username=data['username'],
#                 password=data['password']
#             )
#             user.save()
#             token = Token.objects.create(user=user)
#             print('Try')
            
#             return JsonResponse({'token':str(token)}, status=201)
        
        # except IntegrityError:
        #     ""
        #     print("Exceptions")

        #     return JsonResponse(
        #         {'error': 'username taken. choose another username'},
        #         status=400)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # data is a dictionary
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)
        except IntegrityError:
            return JsonResponse({'error':'username taken. choose another username'}, status=400)