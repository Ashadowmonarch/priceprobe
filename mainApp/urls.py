from django.urls import path,include
from django.conf import settings
from .views import *


urlpatterns = [
    path('',landingPage,name="landingPage"),
    path('login/',loginPage,name="loginPage"),
    path('signup/', signupPage, name="signupPage"),
    path('dashboard/',dashboardPage,name="dashboardPage"),
    path('search/', searchPage,name="searchPage"),
    path('account/',accountPage,name="accountPage"),
    path('saved/',savedPage,name="savedPage"),
    path('trending/',trendingPage,name="trendingPage"),
    path('notifications/',notificationsPage,name="notificationsPage"),
    path('help',helpPage,name="helpPage")
]