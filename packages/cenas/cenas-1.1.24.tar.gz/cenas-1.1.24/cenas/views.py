import os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.cenas1.settings')
application = get_wsgi_application()

def home(request):
    return render(request, 'home.html')

def upload_form(request):
    return render(request, 'upload_form.html')

def run():
    # Change to the project's root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    # Run the migrations
    call_command('migrate', '--settings=webapp.cenas1.settings', verbosity=0)

    # Start the Django development server
    call_command('runserver', '--settings=webapp.cenas1.settings')

if __name__ == '__main__':
    run()