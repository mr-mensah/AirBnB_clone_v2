#!/usr/bin/python3
"""Fabric"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['54.197.122.71', '34.207.61.76']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """do pack"""
    try:
        local("mkdir -p versions")
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """do deploy"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_no_ext = archive_name.split(".")[0]
        path = "/data/web_static/releases/{}".format(archive_no_ext)
        put(archive_path, "/tmp/")
        sudo("mkdir -p {}".format(path))
        sudo("tar -xzf /tmp/{} -C {}".format(archive_name, path))
        sudo("rm /tmp/{}".format(archive_name))
        sudo("mv {}/web_static/* {}".format(path, path))
        sudo("rm -rf {}/web_static".format(path))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {} /data/web_static/current".format(path))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """deploy"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()

