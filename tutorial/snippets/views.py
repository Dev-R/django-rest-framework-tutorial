from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

"""
DEFAULT: Will use snippet_list named function/class try to rename
Class name format= ClassName_ViewType
USAGE: REMOVE _ViewType to run for class based views, for function based: uncomment , return basic url.py
"""

class UserList(generics.ListAPIView):
    # ListAPIView -> Get
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # RetrieveAPIView -> Get by id
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Comment out: if not in use,  Generic class based view
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    # RetrieveUpdateDestroyAPIView ->  Get by id, put, delete
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# Comment out: if not in use,  Generic class based view
class SnippetList(generics.ListCreateAPIView):
      # ListCreateAPIView -> Get/Post
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    