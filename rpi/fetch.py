import urllib
import json
import os


BASEURL = 'http://localhost:8000'
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

# print data['galleries']['0']

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
        urllib.urlretrieve(url, os.path.join(BASE_DIR, title, name))
