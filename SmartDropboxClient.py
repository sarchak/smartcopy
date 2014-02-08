__author__ = 'shrikar'
from cmd import Cmd
from os.path import expanduser

class MyPrompt(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        home = expanduser("~")
        self.data = []
        fd = open(home+"/.smartdropbox/database","r")
        for pattern in fd.readlines():
            self.data.append(pattern.strip("\n"))
        fd.close()
        self.index = 1

    def savefile(self):
        home = expanduser("~")
        fd = open(home+"/.smartdropbox/database","w")
        for pattern in self.data:
            fd.write(pattern+"\n")
        fd.close()

    def do_add(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        print "Adding this pattern to ignore path :  %s" % args
        self.data.append(args)
        self.savefile()

    def do_list(self,args):
        self.index = 1
        if(len(self.data) == 0):
            print "No pattern listed in the database."

        for pattern in self.data:
            print str(self.index) +" ) " + pattern
            self.index += 1

    def do_del(self,args):
        del self.data[int(args)-1]
        self.do_list(0)
        self.savefile()

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit


if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting SmartDropBox Engine...')
