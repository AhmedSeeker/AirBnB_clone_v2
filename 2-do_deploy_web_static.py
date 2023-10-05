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

    if path.exists(archive_path):
        file = archive_path.split("/")[-1]
        filename = file.split(".")[0]
        if put(archive_path, f"/tmp/{file}").failed:
            return False
        folder = f"/data/web_static/releases/{filename}"
        if run(f"mkdir -p {folder}/").failed:
            return False
        if run(f"tar -xzf /tmp/{file} -C {folder}/").failed:
            return False
        if run(f"rm /tmp/{file}").failed:
            return False
        if run(f"mv {folder}/web_static/* {folder}/").failed:
            return False
        if run(f"rm -rf {folder}/web_static").failed:
            return False
        if run(f"rm -rf /data/web_static/current").failed:
            return False
        if run(f"ln -s {folder}/ /data/web_static/current").failed:
            return False
        print("New version deployed!")
        return True
    else:
        return False
