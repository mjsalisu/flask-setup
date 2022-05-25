from flask_setup.methods import install, get_project_name

import os

from distutils.dir_util import copy_tree


def build_app(name):
    allowed_apps = ['api', 'basic', 'website']
    if name in allowed_apps:
        try:
            project = get_project_name()
            requirements = {
                'api':["flask", "flask-marshmallow", "flask-sqlalchemy", "flask-migrate", "flask-httpauth"],
                'basic':["flask", "flask-sqlalchemy", "flask-migrate"],
                'website':["flask"]
            }
            # get the original path to this file even when imported from another file
            path = os.path.dirname(os.path.realpath(__file__))
            # copy relevant app files to project directory
            copy_tree(f'{path}/apps/{name}', '.')
            # rename app directory to project name
            os.rename('projectname', project)
            # open run.py file and replace project name
            with open('run.py', 'r') as f:
                content = f.read()
            with open('run.py', 'w') as f:
                f.write(content.replace('projectname', project))
            # loop through files in project directory and replace projectname with project
            for root, dirs, files in os.walk(project):
                for file in files:
                    if file.endswith('.py') or file.endswith('.html'):
                        with open(os.path.join(root, file), 'r') as f:
                            filedata = f.read()
                        filedata = filedata.replace('projectname', project)
                        with open(os.path.join(root, file), 'w') as f:
                            f.write(filedata)
            # install required packages
            install(requirements.get(name))
            print(f'{name.title()} App built successfully')
            return True
        except Exception as e:
            print(e)
            print(f'Perhaps the project: "{project}" already exists')
    return False