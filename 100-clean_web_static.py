#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents
    of the web_static folder of my AirBnB Clone repo
"""
from fabric.api import put, run, env, local, lcd, cd
from datetime import datetime
from os import path
from shlex import quote
env.hosts = ['100.25.34.143', '54.85.11.239']


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


def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if path.exists(archive_path):
        file = archive_path.split("/")[1]
        filename = file.split(".")[0]
        if put(archive_path, '/tmp/{}'.format(quote(file))).failed:
            return False
        folder = '/data/web_static/releases/{}'.format(quote(filename))
        run('mkdir -p {}/'.format(quote(folder)))
        run("tar -xzf /tmp/{} -C {}/".format(quote(file), quote(folder)))
        run('rm /tmp/{}'.format(quote(file)))
        run('mv {}/web_static/* {}/'.format(quote(folder), quote(folder)))
        run('rm -rf {}/web_static'.format(quote(folder)))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(quote(folder)))
        print("New version deployed!")
        return True
    else:
        return False


def deploy():
    """Fabric script that creates and distributes an archive to web servers"""

    archive = do_pack()
    if not path.isfile(archive):
        return False
    return do_deploy(archive)


def do_clean(number=0):
    """Fabric script that deletes out-of-date archives"""

    try:
        number = int(number)
    except TypeError:
        pass
    number = 2 if number <= 1 else number + 1
    command = " | ".join([
        "ls -t {}",
        "grep {}".format("web_static_*"),
        "tail -n +{}",
        "xargs -I {{}} rm -rf {}/{{}}"])

    local(command.format("versions/", number, "versions/"))

    run(command.format(
        "/data/web_static/releases", number, "/data/web_static/releases"))
