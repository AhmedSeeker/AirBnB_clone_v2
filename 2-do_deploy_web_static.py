#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py)
    that distributes an archive to web servers
"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['100.25.34.143', '54.85.11.239']
env.user = "ubuntu"

def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if exists(archive_path):
        file = archive_path.split("/")[1]
        filename = file.split(".")[0]
        deploy = put(archive_path, f"/tmp/{file}")
        folder = "/data/web_static/releases"
        run(f"mkdir -p {folder}/{filename}/")
        run(f"tar -xzf /tmp/{file} -C {folder}/{filename}/")
        run(f"rm /tmp/{file}")
        run(f"mv {folder}/{filename}/web_static/* {folder}/{filename}/")
        run(f"rm -rf {folder}/{filename}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {folder}/{filename}/ /data/web_static/current")
        return True
    else:
        False
