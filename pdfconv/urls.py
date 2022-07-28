from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('usersignup/',views.usersignup,name='usersignup'),
    path('pdfconv/',views.about,name='about'),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
]