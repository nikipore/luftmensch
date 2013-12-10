from fabric.api import *
import fabric.contrib.project as project

import glob
import os

# Local path configuration (can be absolute or relative to fabfile)
env.build_path = 'output'
env.content_path = 'content'
env.dist_path = 'dist'

# Remote server configuration
env.production = 'luftmensch.net'
env.stage = 'staging.luftmensch.net'

COMPRESS_PATTERN = ('*.html', '*.xml', '*.css', '*.js')

S3_DEFAULT_OPTIONS = (
    '--guess-mime-type',
    '--no-progress',
    '--acl-public',
    "--encoding='UTF-8'",
    "--add-encoding-exts='html,xml,css,js'"
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

def dist(config='publishconf.py'):
    local('pelican -d -s {config} -o {dist_path} {content_path}'.format(
        config=config,
        dist_path=env.dist_path,
        content_path=env.content_path
    ))
    local('rm -rf {dist_path}/theme/.webassets-cache'.format(**env))
    local("find {dist_path} -name '.DS_Store' -exec rm {{}} \;".format(**env))

def compress():
    if not COMPRESS_PATTERN:
        return
    local("find {dist_path} {conditions} -exec gzip -9n {{}} \; -exec mv {{}}.gz {{}} \;".format(
        dist_path=env.dist_path,
        conditions='\( {0} \)'.format(' -o '.join("-name '{0}'".format(pattern) for pattern in COMPRESS_PATTERN))
    ))

def _s3(bucket):
    command = 's3cmd sync {path}/ s3://{bucket}/ {options}'.format(
        path=env.dist_path.rstrip('/'),
        bucket=bucket,
        options=' '.join(S3_DEFAULT_OPTIONS)
    )

    local("{command} --skip-existing --exclude=*.* {include} --add-header='Content-Encoding:gzip'".format(
        command=command,
        include=' '.join("--include='{0}'".format(pattern) for pattern in COMPRESS_PATTERN)
    ))

    local("{command} --cf-invalidate --delete-removed".format(command=command))

def stage():
    dist('stageconf.py')
    compress()
    _s3(env.stage)

def publish():
    dist()
    compress()
    _s3(env.production)
