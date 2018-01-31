import urllib
import json
import os
import datetime


BASEURL = 'http://noticeboard.wncc-iitb.org/'
BASE_DIR = 'Downloads/'


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args))


url = urljoin(BASEURL, 'list/')
response = urllib.urlopen(url)
data = json.loads(response.read())

online_list = []
files_to_delete = []
existing_files = []

print
print "Script running at- " + str(datetime.datetime.now())

for g_index in data['galleries']:
    gallery = data['galleries'][g_index]
    title = gallery['title']
    if not os.path.exists(os.path.join(BASE_DIR, title)):
        os.makedirs(os.path.join(BASE_DIR, title))
    print title
    for p_index in gallery['photos']:
        photo = gallery['photos'][p_index]
        img_url = photo['url']
        url = urljoin(BASEURL, img_url)
        name = photo['name']
        online_list.append((url, os.path.join(BASE_DIR, title, name)))
        # urllib.urlretrieve(url, os.path.join(TEMP_DIR, title, name))

print
print "Online List- " + str(len(online_list))
print online_list

for (dirpath, dirnames, filenames) in os.walk(BASE_DIR):
    for file in filenames:
        file_path = os.path.join(dirpath, file)
        existing_files.append(file_path)
        found = False
        for online_file in online_list:
            if online_file[1] == file_path:
                found = True
                break
        if found is False:
            files_to_delete.append(file_path)
print
print "Existing Files- " + str(len(existing_files))
print existing_files

print
print "Files to delete- " + str(len(files_to_delete))
print files_to_delete


for file in online_list:
    if file[1] not in existing_files:
        urllib.urlretrieve(file[0], file[1])

for file in files_to_delete:
    os.remove(file)


# shutil.rmtree(BASE_DIR)
# os.rename(TEMP_DIR, BASE_DIR)
