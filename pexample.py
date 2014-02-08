import plistlib

d = { 'binary_data':plistlib.Data('This data has an embedded null. \0'),
          }

print plistlib.writePlistToString(d)
print plistlib.writePlist(d,"example.plist")
