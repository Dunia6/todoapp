from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodotoggleCompleteSerializer
from todo.models import Todo
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