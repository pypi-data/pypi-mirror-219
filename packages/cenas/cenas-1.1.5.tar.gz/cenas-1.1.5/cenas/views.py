from django.shortcuts import render
from django.http import HttpResponseRedirect
import subprocess
import os

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')

def run():
    # Start the Django development server
    subprocess.run(['python3', 'manage.py', 'runserver'])
