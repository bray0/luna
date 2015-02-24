# luna
forensic based tool

Gui interface for viewing metadata information from images, bear in mind some of the images out there dont have metadata 
information, so not all images will display exif information

The gui library used is WxPython 2.8, so its worth a while to have WxPython installed before cloning the project

DEPENDENCIES
===============
1. WxPython
2. PIL / Pillow
3. hashlib
4. magic

WXPYTHON link
===========
http://www.wxpython.org/download.php

for 2, 3 & 4 modules you can install this using pip, i.e. in ubuntu  terminal
'#apt-get install python-pip'

USING PIP
===========
>pip search <module name>
>pip install <module name>

i.e. 
>pip install pillow

>pip install magic

do for the same for the other modules hashlib & magic.

the project has only been tested using MacOsx and ubuntu , in theory it should work with other linux derivatives 
one just has to know how to use the package management system or compiling the sources, in theory it should also work 
on windows, though you have to go the great length ensuring that all dependencies are sorted out

Installing
===========
>git clone https://github.com/bray0/luna

>cd luna/

>python main.py

thats it!. 
