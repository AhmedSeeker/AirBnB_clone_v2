#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents
    of the web_static folder of my AirBnB Clone repo
"""
from fabric.api import put, run, env, local
from datetime import datetime
from os import path
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
    if path.isfile(archive_path):
        file = archive_path.split("/")[-1]
        filename = file.split(".")[0]
        put(archive_path, f"/tmp/")
        folder = "/data/web_static/releases"
        run(f"mkdir -p {folder}/{filename}/")
        run(f"tar -xzf /tmp/{file} -C {folder}/{filename}/")
        run(f"rm /tmp/{file}")
        run(f"mv {folder}/{filename}/web_static/* {folder}/{filename}/")
        run(f"rm -rf {folder}/{filename}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {folder}/{filename}/ /data/web_static/current")
        print("New version deployed!")
        return True
    else:
        return False
