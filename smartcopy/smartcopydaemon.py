#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import os
import sys
import threading
from Queue import Queue
from os.path import expanduser

class MyHandler(FileSystemEventHandler):
    def __init__(self,src,dest,dirstocreate,filestocopy,lock):
        self.src = src
        self.dest = dest
        self.dirstocreate = dirstocreate
        self.filestocopy = filestocopy
        self.lock = lock
        print "In handler init"
    def on_created(self, event):
#        home = expanduser("~")
#        if(event.src_path == home+"/.smartdropbox/config"):
#            print "Should reload"
#            fd = open("/tmp/Should_Reload","w+")
#            fd.write("Should reload create")
#            fd.close()

        patterns = re.compile(".class$|.json$|.jar|target|.git")
        if len(patterns.findall(event.src_path)) == 0:
            if(event.is_directory):
                print event.src_path
                self.dirstocreate.put(event.src_path)
            else:
                print event.src_path
                self.filestocopy.put(event.src_path)
    def on_modified(self, event):
        home = expanduser("~")
        if(event.src_path == home+"/.smartdropbox/config"):
            print "Should reload"
            fd = open("/tmp/Should_Reload","w+")
            fd.write("Should reload")
            fd.close()

def runme():
    src = "/tmp/source/"
    dest = "/tmp/destination/"
    home = expanduser("~")
    dirstocreate = Queue()
    filestocopy = Queue()
    lock = threading.Lock()
    handler = MyHandler(src,dest,dirstocreate,filestocopy,lock)
    observer = Observer()
    observer.schedule(handler, path='/tmp/source', recursive=True)
    observer.schedule(handler, path=home+"/.smartdropbox/", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            while(not dirstocreate.empty()):
                dir = dirstocreate.get()
                os.system("mkdir -p " + dest+dir.replace(src,""))
                print "mkdir -p " + dest+dir.replace(src,"")

            while(not filestocopy.empty()):
                file = filestocopy.get()
                print "## cp "+file+" "+dest+file.replace(src,"")
                os.system("cp "+file+" "+dest+file.replace(src,""))

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    try:
        pid = os.fork()
        if pid > 0:
            # Exit parent process
            sys.exit(0)
    except OSError, e:
        print >> sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

        # Configure the child processes environment
    os.chdir("/")
    os.setsid()
    os.umask(0)
    runme()



