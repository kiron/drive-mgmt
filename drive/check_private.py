#!/usr/bin/python

"""
Quick check to dump files listed in your own (private) directory
"""
import sys

#neccesary hack on a mac
sys.path.insert(1, '/Library/Python/2.7/site-packages')

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

try:
    gauth = GoogleAuth()
except:
    print "failed to start auth. packages probably screwed."
    sys.exit()

try:
    gauth.LocalWebserverAuth()
except:
    print "failed to create server! quitting"
    sys.exit()

drive = GoogleDrive(gauth)
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
  print 'title: %s, id: %s' % (file1['title'], file1['id'])
