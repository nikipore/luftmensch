from fabric.api import *
import fabric.contrib.project as project

import glob
import os

# Local path configuration (can be absolute or relative to fabfile)
env.config_path = 'config'
env.build_path = 'output'
env.content_path = 'content'
env.dist_path = 'dist'

env.conf_build = os.path.join(env.config_path, 'build.py')
env.conf_stage = os.path.join(env.config_path, 'stage.py')
env.conf_production = os.path.join(env.config_path, 'production.py')

# Remote server configuration
env.stage = 'staging.luftmensch.net'
env.production = 'luftmensch.net'

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
    local('pelican -s {conf_build} -o {build_path} {content_path}'.format(**env))

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s {conf_build} -o {build_path} {content_path}'.format(**env))

def serve():
    local('cd {build_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

def dist(config=env.conf_production):
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

def _s3(bucket, invalidate=False):
    options = list(S3_DEFAULT_OPTIONS)
    if invalidate:
        options.append('--cf-invalidate')

    command = 's3cmd sync {path}/ s3://{bucket}/ {options}'.format(
        path=env.dist_path.rstrip('/'),
        bucket=bucket,
        options=' '.join(options)
    )

    local("{command} --exclude=*.* {include} --add-header='Content-Encoding:gzip'".format(
        command=command,
        include=' '.join("--include='{0}'".format(pattern) for pattern in COMPRESS_PATTERN)
    ))

    local("{command} --delete-removed".format(
        command=command
    ))

def stage():
    dist(env.conf_stage)
    compress()
    _s3(env.stage)

def production():
    dist()
    compress()
    _s3(env.production, invalidate=True)
