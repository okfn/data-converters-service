from fabric.api import env, task, run
from fabric.decorators import hosts
from fabric.operations import sudo, local


env.hosts = ['okfn@s030.okserver.org']


@task
def restart_supervisor():
    sudo('supervisorctl -c /etc/supervisor/supervisord.conf restart dataconverter')

@task
@hosts('localhost')
def push_code():
    local('git push prod master')

@task
def deploy():
    push_code()
    restart_supervisor()
