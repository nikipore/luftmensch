from fabric.api import *
import fabric.contrib.project as project

import glob
import os

# Local path configuration (can be absolute or relative to fabfile)
env.build_path = 'output'
env.content_path = 'content'
env.dist_path = 'dist'
env.stage_path = 'stage'

# Remote server configuration
production = 'nikipore@pavo.uberspace.de:22'
dest_path = '/var/www/virtual/nikipore/html/'

env.s3 = 'luftmensch'
env.s3_stage = 'staging.luftmensch'

COMPRESS_PATTERN = (
    ('*.html', 'text/html'),
    ('*.xml', 'application/xml'),
    ('*.css', 'text/css'),
    ('*.js', 'text/javascript')
)

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
    local('find {dist_path} -name .DS_Store -exec rm {{}} \;'.format(**env))
    local('rm -rf {dist_path}/theme/.webassets-cache'.format(**env))

def compress():
    for (root, subdirs, _) in os.walk(env.dist_path):
        for (pattern, _) in COMPRESS_PATTERN:
            for filename in glob.glob(os.path.join(root, pattern)):
                local('gzip -9n {0} && mv {0}.gz {0}'.format(filename))

def stage():
    local('rsync --checksum --delete --recursive {dist_path}/ {stage_path}/'.format(
        dist_path=env.dist_path.rstrip('/'),
        stage_path=env.stage_path.rstrip('/')
    ))

def s3_stage():
    s3(env.s3_stage)

def s3_publish():
    s3(env.s3_publish)

def s3(bucket):
    dist()
    compress()
    stage()
    flags = '--progress --acl-public'

    for (pattern, mime_type) in COMPRESS_PATTERN:
        local("s3cmd sync {path}/ s3://{bucket}/ {flags} --exclude=*.* --include={pattern} --mime-type={mime_type} --add-header='Content-Encoding:gzip'".format(
            path=env.stage_path.rstrip('/'),
            bucket=bucket,
            flags=flags,
            pattern=pattern,
            mime_type=mime_type
        ))

    local("s3cmd sync {path}/ s3://{bucket}/ {flags} -M {exclude}".format(
        path=env.stage_path.rstrip('/'),
        bucket=bucket,
        flags=flags,
        exclude=' '.join('--exclude={0}'.format(pattern) for (pattern, _) in COMPRESS_PATTERN)
    ))

@hosts(production)
def publish():
    dist()
    project.rsync_project(
        remote_dir=dest_path.rstrip('/') + '/',
        local_dir=env.dist_path.rstrip('/') + '/',
        delete=True,
        extra_opts='--checksum'
    )
