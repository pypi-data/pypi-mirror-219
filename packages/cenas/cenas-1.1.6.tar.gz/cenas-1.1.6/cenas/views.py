from django.shortcuts import render
import subprocess
import os

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')

def run():
    # Change to the project's root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # Run the migrations
    os.system('python manage.py migrate')

    # Start the Django development server
    os.system('python manage.py runserver')
