from django.shortcuts import render
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
import subprocess
import os

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cenas1.settings')
application = get_wsgi_application()

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')

def run():
    # Change to the project's root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(project_root, 'cenas1'))  # Change to the 'cenas1' directory

    # Run the migrations
    call_command('migrate')

    # Start the Django development server
    subprocess.Popen(['python3', 'manage.py', 'runserver'])

if __name__ == '__main__':
    run()