#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch
from watchdog.events import FileSystemEventHandler
from watchdog.observers.api import EventEmitter
import re
from watchdog.observers.api import EventQueue
from watchdog.observers.polling import PollingEmitter as Emitter
from daemon import Daemon
import os
import sys
import threading
from Queue import Queue


class MyHandler(FileSystemEventHandler):
    def __init__(self,src,dest,dirstocreate,filestocopy,lock):
        self.src = src
        self.dest = dest
        self.dirstocreate = dirstocreate
        self.filestocopy = filestocopy
        self.lock = lock
        print "In handler init"
    def on_created(self, event):
        patterns = re.compile(".class$|.json$|.jar|target|.git")

        print event.src_path
        fd = open("/tmp/fcreate","w")
        fd.write(event.src_path)
        fd.close()

        if len(patterns.findall(event.src_path)) == 0:
            self.lock.acquire()
            if(event.is_directory):
                print event.src_path
#                self.dirstocreate.append(event.src_path)
                self.dirstocreate.put(event.src_path)
            else:
                print event.src_path
#                self.filestocopy.append(event.src_path)
                self.filestocopy.put(event.src_path)
            self.lock.release()
#            if(event.src_path in dirstocreate):
#                dirstocreate.remove(event.src_path)
#            if(event.src_path in filestocopy):
#                filestocopy.remove(event.src_path)


def runme():
    src = "/tmp/source/"
    dest = "/tmp/destination/"
    dirstocreate = Queue()
    filestocopy = Queue()
    lock = threading.Lock()
    handler = MyHandler(src,dest,dirstocreate,filestocopy,lock)
    observer = Observer()
    observer.schedule(handler, path='/tmp/source', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            #for dir in dirstocreate:
            while(not dirstocreate.empty()):
                dir = dirstocreate.get()
                os.system("mkdir -p " + dest+dir.replace(src,""))
                print "mkdir -p " + dest+dir.replace(src,"")
            lock.acquire()
            #dirstocreate = []
            lock.release()
#            for file in filestocopy:
            while(not filestocopy.empty()):
                file = filestocopy.get()
                print "## cp "+file+" "+dest+file.replace(src,"")
                os.system("cp "+file+" "+dest+file.replace(src,""))
            lock.acquire()
            #filestocopy = []
            lock.release()

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



