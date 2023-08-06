import os
import sys


def create_project(project_name):
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir)
    
    app_dir = os.path.join(project_dir, 'app')
    os.makedirs(app_dir)
    open(os.path.join(app_dir, '__init__.py'), 'w').close()
    
    open(os.path.join(project_dir, '__init__.py'), 'w').close()
    open(os.path.join(project_dir, 'manage.py'), 'w').close()
    
    views_dir = os.path.join(app_dir, 'views')
    os.makedirs(views_dir)
    
    static_dir = os.path.join(app_dir, 'static')
    os.makedirs(static_dir)
    
    errors_dir = os.path.join(app_dir, 'errors')
    os.makedirs(errors_dir)
    
    utils_dir = os.path.join(app_dir, 'utils')
    os.makedirs(utils_dir)
    
    open(os.path.join(app_dir, 'main.py'), 'w').close()
    open(os.path.join(app_dir, '__init__.py'), 'w').close()
    open(os.path.join(app_dir, 'wsgi.py'), 'w').close()
    
    settings_py_code = '''
# settings.py config

HOST = "127.0.0.1"  # default host by ZyloWeb on localhost
PORT = 8000 # default port by ZyloWeb on 8000
DEBUG = True # default debug value True for development

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0'] # You can add more hosts as per your requirements

# Zylo provides a inbuilt database engine @nexus, NexusDB developed by @PyDev using Json/Application.
# @nexus is a fully managed and structured database and also compatible for production usage with,
# app.config['SET_APP_MODE'] = "Production"
# db.set_app(app.config['SET_APP_MODE'])

# Default configuration for @nexus 

DATABASES = {
    'default': {
        'ENGINE': 'zylo.db.backends.nexus', # default database engine Nexus
        'NAME': 'YOUR_DB_NAME',
        'USER': 'USERNAME',
        'PASSWORD': 'PASSWORD_FOR_DB',
        'HOST': 'localhost'
    }
}

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
TEMPLATE_ENGINE = '/views'
'''
    with open(os.path.join(app_dir, 'settings.py'), 'w') as f:
        f.write(settings_py_code)
    
    open(os.path.join(app_dir, '.env'), 'w').close()
    
    config_json_code = f'''
{{
    "name": "{project_name}",
    "version": "1.0.0",
    "description": "Description of your project",
    "author": "Your Name",
    "email": "your@email.com",
    "app": {{
        "name": "Your App Name",
        "description": "Description of your app",
        "server": [
        {{ 
            "server": "alice conf.app.py",
            "server:prod": "bind 127.0.0.0:8000 *conf",
            "server:static": "zylo @admin.commit *server static()",
            "server:daemon": "**config(daemon) --lts"
        }}
        ],
        "routes": [
        {{
            "url": "/",
            "methods": ["GET", "POST"],
            "secure": true,
            "handler": "app.home"
        }}
        ],
        "dependencies": [
        {{
            "ZyloAdmin": "2.0.2 -2.0988 byte",
            "Zylo": "2.0.1 -36910 byte",
            "Zylo.session": "1.1.1 -35446 byte",
            "Zylo.JwT": "1.1.5 -78263 byte",
            "Zylo.blueprint": "1.1.0 -89366 byte",
            "Zylo.chiper": "1.1.0 -102235 byte",
            "nexusdb": "2.2.6 -500983349 byte" 
        }}
        ]
    }}
}}
'''
    with open(os.path.join(app_dir, 'config.json'), 'w') as f:
        f.write(config_json_code)
    
    views_file = os.path.join(views_dir, 'index.html')
    with open(views_file, 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Thank you for using Zylo web framework!</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.16/dist/tailwind.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mx-auto">
        <h1 class="text-4xl font-bold mt-10">Thank you for using Zylo web framework!</h1>
    </div>
</body>
</html>
''')
    
    static_css_dir = os.path.join(static_dir, 'css')
    os.makedirs(static_css_dir)
    
    static_js_dir = os.path.join(static_dir, 'js')
    os.makedirs(static_js_dir)
    
    main_py_code = '''
from zylo import Zylo, Response, render_template, NotFound
from zylo.blueprint import Blueprint

app = Zylo()
blueprint = Blueprint('blog', __name__, url_prefix='/blog')

@app.route("/")
def home(request):
    return render_template('index.html')

@blueprint.route('/post')
def blog_post(request):
    return Response('Welcome to Blueprint route http://127.0.0.1:8000/blog/post')

@app.route('/static/<filename>')
def serve_static_file(filename):
    try:
        return app.serve_static(filename)
    except NotFound:
        return Response('File not found', status=404)


# Register the blueprint with the app
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()
'''
    with open(os.path.join(app_dir, 'main.py'), 'w') as f:
        f.write(main_py_code)
    
    wsgi_py_code = '''
from main import app

if __name__ == "__main__":
    app.run()
'''
    with open(os.path.join(app_dir, 'wsgi.py'), 'w') as f:
        f.write(wsgi_py_code)
    
    manage_py_code = '''
# Add your manage code here:
# Example usage

from main.app import app

@app.route("/", methods=['GET'])
def home(request):
    return Response("welcome to Zylo")
'''
    with open(os.path.join(project_dir, 'manage.py'), 'w') as f:
        f.write(manage_py_code)


def startproject(command):
    command_parts = command.split()
    
    if command_parts[0] == 'startproject' and command_parts[1] == '-i' and len(command_parts) == 3:
        project_name = command_parts[2]
        create_project(project_name)
        print(f"Project '{project_name}' created successfully!")
    else:
        print("Invalid command. Please use the 'startproject -i <project_name>' format.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py startproject -i <project_name>")
    else:
        command = " ".join(sys.argv[1:])
        startproject(command)

if __name__ == "__main__":
    main()
