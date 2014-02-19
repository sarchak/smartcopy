#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import os
import sys
import subprocess
import smartutils
import threading
from Queue import Queue
from os.path import expanduser
from smartutils import get_config
from smartutils import get_db
from smartutils import reload_config
from smartutils import get_patterns
from smartutils import quote

class MyHandler(FileSystemEventHandler):
    def __init__(self,src,dest,dirstocreate,filestocopy):
        self.src = src
        self.dest = dest
        self.dirstocreate = dirstocreate
        self.filestocopy = filestocopy
        print get_patterns()
        self.patterns = re.compile(get_patterns())

    def on_any_event(self, event):
        print "wtf"
        
    def on_created(self, event):
        if len(self.patterns.findall(event.src_path)) == 0:
            if(event.is_directory):
                print event.src_path
                self.dirstocreate.put(event.src_path)
            else:
                print event.src_path
                self.filestocopy.put(event.src_path)


    def on_moved(self, event):
        self.on_created(event)

    def on_modified(self, event):
        print "Modified"
        home = expanduser("~")
        if(event.src_path == get_config()):
            self.src,self.dest = reload_config()
        if(event.src_path == get_db()):
            self.patterns = re.compile(get_patterns())
        self.on_created(event)
        
def runme():
    src,dest = reload_config()
    home = expanduser("~")
    dirstocreate = Queue()
    filestocopy = Queue()
    handler = MyHandler(src,dest,dirstocreate,filestocopy)
    observer = Observer()
    observer.schedule(handler, path=src, recursive=True)
    observer.schedule(handler, path=home+"/.smartcopy/", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            while(not dirstocreate.empty()):
                dir = dirstocreate.get()
                subprocess.call(["mkdir","-p",quote(dest+dir.replace(src,""))])
                print "mkdir -p " + dest+quote(dir.replace(src,""))

            while(not filestocopy.empty()):
                file = filestocopy.get()
                print "## cp "+quote(file)+" "+dest+quote(file.replace(src,""))
                subprocess.call(["cp",file,dest+file.replace(src,"")])

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    try:
        pid = os.fork()
        if pid > 0:

            sys.exit(0)
    except OSError, e:
        print >> sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

        # Configure the child processes environment
    home = expanduser("~")
    smartdir = home+"/.smartcopy"
    print smartdir
    if(not os.path.exists(smartdir)):
        subprocess.call(["mkdir","-p",quote(smartdir)])
        if(not os.path.exists(get_config())):
            subprocess.call(["touch",get_config()])
        if(not os.path.exists(get_db())):
            subprocess.call(["touch ",get_db()])

    os.chdir("/")
    os.setsid()
    os.umask(0)
    runme()



