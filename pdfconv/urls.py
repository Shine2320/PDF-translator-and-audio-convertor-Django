from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('pdfconv/',views.about,name='about')
]