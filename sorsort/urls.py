from django.urls import path

from . import views

app_name = "sorsort"

urlpatterns = [
    path('home', views.home, name='home'),
    path('rush', views.first, name='first'),
    path('phil', views.second, name='second'),
    path('sister', views.third, name='third'),
	#path('upload_csv', views.upload_csv, name='upload_csv'),

]
