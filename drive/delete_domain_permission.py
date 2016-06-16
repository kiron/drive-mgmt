#!/usr/bin/python
"""Delete domain permission from your Google Drive files.

The reason why I created this script is so that I can use this script to
recursively remove the domain permission item from all files.

By default, Google Drive will share files to all users in the domain (this
setting is recognised as the domain permission type for the file in
Google Drive). I don't really want certain files to be shared this way, but
there is no easy way recursively fix this in Google Drive, so that is why
this script is created.

#on macos, you'll need to install pydrive using this:
pip install PyDrive --ignore-installed six

you'll need this to figure this out:
http://pythonhosted.org/PyDrive/quickstart.html#authentication
-> note!!! chose "other" instead of "web application"
-> download the JSON token and save it to client_secrets.json in the working dir


Usage:

    python delete_domain_permission.py FOLDER_ID

FOLDER_ID is the alpha-numeric ID that is found on the URL, e.g.

    0B217z8PSk4D4dU7ZeHdtUmxsdFk

If you want to scan through all the folders you can use "root" as the
FOLDER_ID.

Dependencies:
 * PyDrive==1.0.0

Tested with Python2.7.6

"""
import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

drive = None

logf = open("error.log", "wb")

##main loop
def main(file_id):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    global drive
    drive = GoogleDrive(gauth)

    list_files(gdrive_get_children(file_id))

##check for non ascii characters
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def list_files(results, tab_count=0):
    for file_list in results:
        for f in file_list:
            print_file(f, tab_count)
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                list_files(gdrive_get_children(f['id']), tab_count=tab_count+1)


def gdrive_get_children(file_id):
    return drive.ListFile(
        {'q': "'{}' in parents".format(file_id), 'maxResults': 100})


def print_file(f, tab_count):
    s_perms = f.auth.service.permissions()
    perms = s_perms.list(fileId=f['id']).execute()
    unique_perm_types = list(set([p['type'] for p in perms['items']]))

    def _print_item(prefix):
        if(is_ascii(f['title'])):
            print('{}{}: {}, id: {}, perm: {}'.format(
                '\t' * tab_count, prefix, f['title'], f['id'], unique_perm_types))
        else:
            logf.write("%s" % f['title'].encode('utf-8'))

    if f['mimeType'] == 'application/vnd.google-apps.folder':
        _print_item('FOLDER')
    else:
        _print_item(' + FILE')

    for p in perms['items']:
        if p['type'] == 'domain':
            print('DELETING domain permission, {}'.format(p['id']))
            try:
                s_perms.delete(fileId=f['id'], permissionId=p['id']).execute()
            except:
                pass


if __name__ == '__main__':
    if len(sys.argv)>1:
        file_id = sys.argv[1]
        main(file_id)
        logf.close()
    else:
        print "usage: ./delete_domain_permission.py <FOLDER_ID>"
