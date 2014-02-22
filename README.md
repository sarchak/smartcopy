smartcopy
=========

Intelligent layer on top of existing cloud storage

### Requirements
   
   * Unix based OS with fork support and support for watching filesystem changes through inotify, FSEvents or  kqueue.
   * python 2.7 and above
   
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

   * sudo easy_install smartcopy

#### Method 2 ( For current development branch)
   * git clone https://github.com/sarchak/smartcopy.git
   * cd smartcopy
   * sudo python setup.py install 

### Starting the daemon

<pre><code>
Shrikars-MacBook-Pro:~ shrikar$ smartcopyd
Shrikars-MacBook-Pro:~ shrikar$ smartcopy
/Users/shrikar/.smartcopy
Starting SmartCopy Engine...
smartcopy> add .*.jpg
Adding this pattern to ignore path :  .*.jpg
smartcopy> add .*.pdf
Adding this pattern to ignore path :  .*.pdf
smartcopy> add .*.jar
Adding this pattern to ignore path :  .*.jar
smartcopy>
</code></pre>

  
The above command will create a directory called SmartCopy in your home folder feel free to drag it to the finder sidebar or where ever its convenient for you to copy files.

### Important : While syncing files DO NOT COPY OR MOVE files directly to the dropbox folder instead copy/move to SmartCopy folder which will filter the files and sync's them to the dropbox folder.

[More Info](http://shrikar.com/blog/2014/02/21/smartcopy-intelligent-layer-on-top-of-existing-cloud-storage/)
