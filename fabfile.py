from fabric.api import *
import fabric.contrib.project as project

import glob
import os

# Local path configuration (can be absolute or relative to fabfile)
env.build_path = 'output'
env.content_path = 'content'
env.dist_path = 'dist'

# Remote server configuration
production = 'nikipore@pavo.uberspace.de:22'
dest_path = '/var/www/virtual/nikipore/html/'

env.s3 = 'luftmensch'
env.s3_stage = 'staging.luftmensch'

COMPRESS_PATTERN = ('*.html', '*.xml', '*.css', '*.js')

def clean():
    for path in (env.build_path, env.dist_path):
        if os.path.isdir(path):
            local('rm -rf {0}'.format(path))

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
    local('pelican -d -s publishconf.py -o {dist_path} {content_path}'.format(**env))
    local('rm -rf {dist_path}/theme/.webassets-cache'.format(**env))
    local("find {dist_path} -name '.DS_Store' -exec rm {{}} \;".format(**env))

def compress():
    local("find {dist_path} {conditions} -exec gzip -9n {{}} \; -exec mv {{}}.gz {{}} \;".format(
        dist_path=env.dist_path,
        conditions='\( {0} \)'.format(' -o '.join("-name '{0}'".format(pattern) for pattern in COMPRESS_PATTERN))
    ))

def s3(bucket):
    dist()
    compress()

    flags = '--progress --acl-public'

    local("s3cmd sync {path}/ s3://{bucket}/ {flags} --exclude=*.* {include} --add-header='Content-Encoding:gzip'".format(
        path=env.dist_path.rstrip('/'),
        bucket=bucket,
        flags=flags,
        include=' '.join('--include={0}'.format(pattern) for pattern in COMPRESS_PATTERN)
    ))

    local("s3cmd sync {path}/ s3://{bucket}/ {flags} --delete-removed".format(
        path=env.dist_path.rstrip('/'),
        bucket=bucket,
        flags=flags
    ))

def s3_stage():
    s3(env.s3_stage)

def s3_publish():
    s3(env.s3_publish)

@hosts(production)
def publish():
    dist()
    project.rsync_project(
        remote_dir=dest_path.rstrip('/') + '/',
        local_dir=env.dist_path.rstrip('/') + '/',
        delete=True,
        extra_opts='--checksum'
    )
