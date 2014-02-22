__author__ = 'shrikar'
from os.path import expanduser
import os
def get_config():
    home = expanduser("~")
    return home+"/.smartcopy/config"

def get_db():
    home = expanduser("~")
    return home+"/.smartcopy/database"


def reload_config():
    fd = open(get_config(),"r")
    line = fd.readline()
    src = line.split("=")[1].strip("\n")
    line = fd.readline()
    dest = line.split("=")[1].strip("\n")
    fd.close()
    if(not os.path.exists(src)):
        os.system("mkdir -p "+src)
    if(not os.path.exists(dest)):
        os.system("mkdir -p "+dest)

    return (src,dest)

def get_patterns():
    fd = open(get_db(),"r")
    tmp = []
    for pattern in fd.readlines():
        tmp.append(pattern.strip("\n"))
    fd.close()
    return "|".join(tmp)

def quote(argument):
    return argument.replace(" ","\ ").replace("*","\*").replace("$","\$").replace("^","\^")