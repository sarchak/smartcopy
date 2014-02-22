from setuptools import setup

setup(name='smartcopy',
      version='0.6',
      description='Intelligent layer on top of any cloud storage provider like Dropbox/Box/Google Drive',
      url='http://github.com/sarchak/smartcopy',
      author='Shrikar Archak',
      author_email='shrikar84@gmail.com',
      license='MIT',
      install_requires=['watchdog>=0.7.1'],
      scripts=['smartcopy/smartcopy','smartcopy/smartcopyd'],
      packages=["smartutils"],
      zip_safe=False)
