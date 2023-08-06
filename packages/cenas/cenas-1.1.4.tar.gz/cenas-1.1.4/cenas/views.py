from django.shortcuts import render
from django.http import HttpResponseRedirect
import subprocess
import os

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')

def run(request):
    # Change to the project's root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Start the Django development server
    subprocess.run(['python', 'manage.py', 'runserver'])
