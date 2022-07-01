from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User
'''
A serializer class is very similar to a Django Form class, 
and includes similar validation flags on the various fields, 
such as required, max_length and default.
'''
# class SnippetSerializer(serializers.Serializer):
#     '''
#     Notice using of serializers.Serializer make it explicit on what we
#     want to Serialize
#     '''
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

class SnippetSerializer_Model(serializers.ModelSerializer):
    '''
    Notice using 'ModelSerializer' is less explicit and better than 'Serializer
    as SnippetSerializer(serializers.Serializer) class is replicating a lot of information 
    that's also contained in the Snippet model
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'owner','style']
    '''
    It's important to remember that ModelSerializer classes don't do 
    anything particularly magical, 
    they are simply a shortcut for creating serializer classes:
    An automatically determined set of fields.
    Simple default implementations for the create() and update() methods.
    '''

class UserSerializer_Model(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']



'''
                    The HyperlinkedModelSerializer class is similar to the ModelSerializer 
                    class except that it uses hyperlinks to represent relationships, rather than primary keys.
                    https://stackoverflow.com/questions/33421147/what-is-the-benefit-of-using-a-hyperlinkedmodelserializer-in-drf
'''

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    '''
    The HyperlinkedModelSerializer has the following differences from ModelSerializer:
        It does not include the id field by default.
        It includes a url field, using HyperlinkedIdentityField.
        Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    The HyperlinkedModelSerializer has the following differences from ModelSerializer:
        It does not include the id field by default.
        It includes a url field, using HyperlinkedIdentityField.
        Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.
    '''
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']