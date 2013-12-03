from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.build_path = 'output'
env.content_path = 'content'
env.dist_path = 'dist'

# Remote server configuration
production = 'nikipore@pavo.uberspace.de:22'
dest_path = '/var/www/virtual/nikipore/html/'

def clean():
    for path in (env.build_path, env.dist_path):
        if os.path.isdir(path):
            local('rm -rf {0}'.format(os.path.join(path, '*')))
        local('mkdir {0}'.format(path))

def build():
    local('pelican -s pelicanconf.py -o {build_path} {content_path}'.format(**env))

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py -o {build_path} {content_path}'.format(**env))

def serve():
    local('cd {build_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

def dist():
    local('pelican -s publishconf.py -o {dist_path} {content_path}'.format(**env))

@hosts(production)
def publish():
    dist()
    project.rsync_project(
        remote_dir=dest_path.rstrip('/') + '/',
        exclude=".DS_Store",
        local_dir=env.dist_path.rstrip('/') + '/',
        delete=True
    )
