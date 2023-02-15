from django.urls import path, include
from rest_framework import routers
from . import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()

urlpatterns = [
    path('madeby', views.MadeByView.as_view()),
    path('login', views.LoginView.as_view()),
    path('blogpost', views.BlogPostView.as_view()),
    path('hiddenblogpost', views.ShowHiddenBlogPostView.as_view()),
    path('showusers', views.ShowUsersView.as_view()),
]
