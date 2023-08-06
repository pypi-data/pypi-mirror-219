from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('upload/',views.upload_form, name='upload_form'),
    # Add more URL patterns here
]
