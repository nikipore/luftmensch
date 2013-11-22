from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
env.content_path = 'content'

# Remote server configuration
production = 'nikipore@pavo.uberspace.de:22'
dest_path = '/var/www/virtual/nikipore/html/'

def clean():
    if os.path.isdir(env.deploy_path):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    local('pelican -s pelicanconf.py {content_path}'.format(**env))

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py {content_path}'.format(**env))

def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

def preview():
    local('pelican -s publishconf.py {content_path}'.format(**env))

@hosts(production)
def publish():
    preview()
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=env.deploy_path.rstrip('/') + '/',
        delete=True
    )
