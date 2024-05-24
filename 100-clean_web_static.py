#!/usr/bin/python3
import os
from fabric.api import *

env.hosts = ['52.207.79.6', '34.234.193.197']


def do_clean(number=0):
    """Deletes an out-of-date archive.

    Args:
        number (int): The No. of archives to keep.

    If number is 0 or 1, keeps the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
