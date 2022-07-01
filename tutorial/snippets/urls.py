from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.urls import path, include
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers
from rest_framework.routers import DefaultRouter


'''
    Binding ViewSets to URLs explicitly(Not needed since we use viewset)<The conventions for wiring up resources into views and urls can be handled automatically>
    handler methods only get bound to the actions when we define the URLConf.
    Notice how we're creating multiple views from each ViewSet class, by binding the http methods to the required action for each view.
'''
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

'''
    Now that we've bound our resources into concrete views, we can register the views with the URL conf as usual.
'''
urlpatterns_explict = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

'''
    Because we're using ViewSet classes rather than View classes, we actually don't need to design the URL conf ourselves.
    The conventions for wiring up resources into views and urls can be <handled automatically, using a Router class>. 
'''
# Create a router and register our viewsets with it.
router = DefaultRouter() # The DefaultRouter class  automatically creates the API root view for us,
router.register(r'snippets', views.SnippetViewSet,basename="snippet") # Registering the viewsets with the router is similar to providing a urlpattern. 
router.register(r'users', views.UserViewSet,basename="user") # We include two arguments - the URL prefix for the views, and the viewset itself.

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# Uncomment for function based view
# urlpatterns = [
#     path('snippets/', views.snippet_list),
#     path('snippets/<int:pk>/', views.snippet_detail),
# ]
