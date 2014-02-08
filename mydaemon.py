__author__ = 'shrikar'
from watchdog.utils import DaemonThread
from watchdog.observers.api import EventEmitter
from  watchdog.observers.api import ObservedWatch
from watchdog.observers.api import EventQueue
import time
import os
class MyEmitter(DaemonThread):
    def start(self):
        print "In start"

    def run(self):
        while True:
            print "hello there"
            time.sleep(1)


if __name__ == "__main__":

#    event_queue = EventQueue()
#    watch = ObservedWatch("/tmp/source", True)
#    emitter = EventEmitter(event_queue, watch, timeout=0.2)
#    emitter.start()
#    os.system("echo hi > /tmp/source/hi")
#    while not event_queue.empty():
#        print event_queue.get().src_path
    my = MyEmitter()
    my.setDaemon("bingo")
    my.setDaemon(False)
    if(my.isDaemon()):
        print "Its a daemon"
    else:
        print "Its not a daemon"