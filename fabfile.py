# -*- coding: utf-8 -*-

from fabric.api import run, env, local
from fabric.contrib.project import rsync_project

env.host=[
        'zhouquan@121.41.72.162:52113',
    ]
env.password = {
        'zhouquan@121.41.72.162:52113': 'zhouquan!@#$%^',
        }

def host_type():
    run('uname -s')

def release():
    #local("git co RELEASE")
    rsync_project(remote_dir='/home/zhouquan/project/ebooking',
            local_dir='./',
            delete=True,
            extra_opts="--exclude-from '.gitignore'")
    #local("git co master")
