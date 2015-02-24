#!/usr/bin/env python 2

import os
import sys
import time
import magic
import hashlib

#m = magic.Magic(magic_file=r'C:\magicfiles\magic', mime=True) in windows specify the location of the magic file
m = magic.Magic(mime=True)
def md5sum(filename):
	md5 = hashlib.md5()
	with open(filename, 'rb') as f:
		for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
			md5.update(chunk)
	return md5.hexdigest()

def sha1sum(filename):
	sha1 = hashlib.sha1()
	with open(filename, 'rb') as f:
		for chunk in iter(lambda: f.read(128 * sha1.block_size), b''):
			sha1.update(chunk)
	return sha1.hexdigest()

def sha256sum(filename):
	sha256 = hashlib.sha256()
	with open(filename, 'rb') as f:
		for chunk in iter(lambda: f.read(128 * sha256.block_size), b''):
			sha256.update(chunk)
	return sha256.hexdigest()

def getMtime(filename):
	return time.ctime(os.path.getmtime(filename))

def getAtime(filename):
	return time.ctime(os.path.getatime(filename))

def getCtime(filename):
	return time.ctime(os.path.getctime(filename))

def getFsize(filename):
	return os.path.getsize(filename)

