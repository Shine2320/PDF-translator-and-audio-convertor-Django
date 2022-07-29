from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('usersignup/',views.usersignup,name='usersignup'),
    # path('pdf_convert_to_audio/',views.pdf_convert_to_audio,name='pdf_convert_to_audio'),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("user_home", views.user_home, name= "user_home"),
    path("user_pdf_upload", views.user_pdf_upload, name= "user_pdf_upload"),
    path("user_audio_download", views.user_audio_download, name= "user_audio_download"),
    path("user_audio_play", views.user_audio_play, name= "user_audio_play"),
]