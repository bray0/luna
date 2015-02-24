#!/usr/bin/env python2

from CSVManager import CSVManager
from PIL import Image #pillow
from PIL.ExifTags import TAGS
import sys
import re

#filename = sys.argv[1]

def dataToList(data):
    somelist = []
    finalist = []
    for k, v in data.items():
        somelist = [str(k), str(v)]
        finalist.append(somelist)
    return finalist

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def main():
	try:
		data = get_exif(filename)
		csvhandler = CSVManager()
		newList = csvhandler.dataToList(data)
		csvhandler.HTMLGenerator(newList, filename)
		csvhandler.CSVWriter(newList)
	except:
		print
		print "Bump :( No metadata found!"


if __name__ == "__main__":
	main()
