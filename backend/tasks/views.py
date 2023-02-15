from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from .models import BlogPost
from rest_framework import generics
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import connection

# Input Serializers
from .serializers import LoginSerializer
# Output Serializers
from .serializers import BlogPostSerializer


class MadeByView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({'MadeBy': 'Julian Korgol, https://github.com/JulianKorgol'}, status=HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # login(request, user)
                # return Response(status=HTTP_200_OK)
                return Response({'username': str(user.username), 'success': True}, status=HTTP_200_OK)
        return Response(None, status=HTTP_401_UNAUTHORIZED)


class BlogPostView(generics.GenericAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        post_id = request.GET.get('id')
        if post_id is None or post_id == '':
            return Response({'error': 'The parameter is required'}, status=HTTP_400_BAD_REQUEST)

        try:
            blog_post = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return Response(None, status=HTTP_404_NOT_FOUND)

        if blog_post.public == False:
            return Response({'error': 'Post is non-public'}, status=HTTP_401_UNAUTHORIZED)

        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data, status=HTTP_200_OK)


# SQL Injection
class ShowHiddenBlogPostView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        post_id = request.GET.get('id')
        if post_id is None or post_id == '':
            return Response({'error': 'The parameter is required'}, status=HTTP_400_BAD_REQUEST)

        try:
            cursor = connection.cursor()
            sql_query = 'SELECT * FROM tasks_blogpost WHERE id = ' + post_id + ' and public = 1'
            cursor.execute(sql_query)
            blog_post = cursor.fetchone()
        except BlogPost.DoesNotExist:
            return Response(None, status=HTTP_404_NOT_FOUND)

        if blog_post is None:
            return Response(None, status=HTTP_404_NOT_FOUND)

        blog_post_dict = {}
        blog_post_dict['id'] = blog_post[0]
        blog_post_dict['title'] = blog_post[1]
        blog_post_dict['content'] = blog_post[2]
        blog_post_dict['public'] = blog_post[3]
        return Response({'post': blog_post_dict}, status=HTTP_200_OK)


# SQL Injection 2
class ShowUsersView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        endpoint_username = request.GET.get('username')
        if endpoint_username is None or endpoint_username == '':
            return Response({'error': 'The parameter "username" is required'}, status=HTTP_400_BAD_REQUEST)

        try:
            cursor = connection.cursor()
            sql_query = "SELECT * FROM auth_user WHERE username = '" + endpoint_username + "'" + " and password = 'pbkdf2_sha256$390000$eVgb1KXKMBbp95X54QmaJ4$U92I0czPONjYdUwhh9ckOTBvZAsbG1SFmBBQrjw+j50='"
            cursor.execute(sql_query)
            endpoint_users = cursor.fetchone()
        except User.DoesNotExist:
            return Response(None, status=HTTP_404_NOT_FOUND)

        if endpoint_users is None:
            return Response(None, status=HTTP_404_NOT_FOUND)

        endpoint_users_dict = {}
        endpoint_users_dict['id'] = endpoint_users[0]
        endpoint_users_dict['username'] = endpoint_users[1]
        endpoint_users_dict['password'] = endpoint_users[2]
        return Response({'user': endpoint_users_dict}, status=HTTP_200_OK)
