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
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
"""
DEFAULT: Will use snippet_list named function/class try to rename
Class name format= ClassName_ViewType
USAGE: REMOVE _ViewType to run for class based views, for function based: uncomment , return basic url.py
"""


'''

    ModelViewSet inherited all most all mixins so it provides default list,create,update etc.. action methods and GenericViewSet
    i.e:
        class ModelViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):1
                """
                A viewset that provides default create(),retrieve(),update(),
                partial_update(), destroy() and list() actions. That are inherited from GenericViewSet, mixins
                """
                pass

                                ---IMPORTANT---
    ***THE URLS FOR CUSTOM ACTIONS BY DEFAULT DEPEND ON THE METHOD NAME ITSELF***
    Using viewsets can be a really useful abstractio It helps ensure that URL conventions will be consistent across your API, minimizes the amount of code you need to write

'''
# Only used for explict not in viewsetss
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })





class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions. that constructs (UserList, UserDetail)-Generics
    * ReadOnlyModelViewSet class automatically provide the default 'read-only' operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList_Generics(generics.ListAPIView):
    # ListAPIView -> Get
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail_Generics(generics.RetrieveAPIView):
    # RetrieveAPIView -> Get by id
    queryset = User.objects.all()
    serializer_class = UserSerializer





class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions. that constructs (SnippetDetail, SnippetList, SnippetHighlight)-Generics

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    '''
    @action decorator to create a custom action, named highlight.
    This decorator can be used to add any custom endpoints that don't fit into the standard create/update/delete style.
    Custom actions which use the @action decorator will respond to GET requests by default.
     We can use the methods argument if we wanted an action that responded to POST requests.
     i.e: @action(methods=['GET'], detail=False, url_path='get-courses')
    '''
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





# Comment out: if not in use,  Generic class based view
class SnippetDetail_Generics(generics.RetrieveUpdateDestroyAPIView):
    # RetrieveUpdateDestroyAPIView ->  Get by id, put, delete
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# Comment out: if not in use,  Generic class based view
class SnippetList_Generics(generics.ListCreateAPIView):
      # ListCreateAPIView -> Get/Post
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetHighlight_Generics(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    