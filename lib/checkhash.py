#!/usr/bin/env python2

import hashlib
import sys

#fileName = sys.argv[1]

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

def main():
	print
	print "MD5:    ",md5sum(fileName)
	print "SHA1:   ",sha1sum(fileName)
	print "SHA256: ",sha256sum(fileName)

if __name__ == "__main__":
	main()
