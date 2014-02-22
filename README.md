smartcopy
=========

Intelligent layer on top of existing cloud storage

### Design

I followed a similar method to .gitignore and hence decided to have a list of all the pattern that need to be ignored from syncing

#### Example

   * .*.jar  : Ignore all the files containing .jar
   * .class$ : Ignore all the files ending with .class
   * ^Bingo  : Ignore all the files starting with Bingo

For more information on using regular expression please check the python regex documentation.

### Components

   * ) smartcopyd : SmartCopy Daemon
smartcopydaemon monitors for changes to a directory , filter the files according to the ignore patterns and sync's to the cloud storage.

   * ) smartcopy : SmartCopy Client
smartcopy allows you to change the config file and modify any ignore pattern rules.

[Python regex](http://docs.python.org/2/library/re.html)


### Installation

#### Method 1 ( For using the latest stable branch)
   1 sudo easy_install smartcopy

#### Method 2 ( For current development branch)
   1 git clone https://github.com/sarchak/smartcopy.git
   2 cd smartcopy
   3 sudo python setup.py install 

