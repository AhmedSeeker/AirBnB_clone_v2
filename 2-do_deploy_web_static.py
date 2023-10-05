#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents
    of the web_static folder of my AirBnB Clone repo
"""
from fabric.api import put, run, env, local, task
from datetime import datetime
from os import path
from shlex import quote
env.hosts = ['100.25.34.143', '54.85.11.239']
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


@task
def do_pack():
    """ Generate a .tgz archive from the contents of the web_static folder """

    """folder to store all archives"""
    local("mkdir -p versions")

    """archive name: web_static_<year><month><day><hour><minute><second>.tgz"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive = f"versions/web_static_{timestamp}.tgz"
    try:
        local(f"tar -cvzf {archive} web_static")
        return archive
    except Exception:
        return None


@task
def do_deploy(archive_path):
    """Distribute an archive to web servers"""

    if path.exists(archive_path):
        file = archive_path.split("/")[1]
        filename = file.split(".")[0]
        if put(archive_path, '/tmp/{}'.format(quote(file))).failed:
            return False
        folder = "/data/web_static/releases/{}".format(filename)
        run("rm -rf {}/".format(folder))
        run("mkdir -p {}/".format(folder))
        run("tar -xzf /tmp/{} -C {}/".format(file, folder))
        run("rm /tmp/{}".format(quote(file)))
        run("mv {}/web_static/* {}/".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(folder))
        print("New version deployed!")
        return True
    else:
        return False
