try:
    from urllib import urlopen, urlretrieve
except ImportError:
    # Python 3 fallback
    from urllib.request import urlopen, urlretrieve
import json
import os
import datetime


# Where is the RPi set up.
# If set to "h9" allows access to all private galleries that have title
# starting with "h9"
FROM = "hostel9"

BASEURL = 'http://noticeboard.wncc-iitb.org/'
BASE_DIR = 'Downloads/'


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args))


def fetch_data():
    url = urljoin(BASEURL, 'list/', '?from=' + FROM)
    response = urlopen(url)
    data = json.loads(response.read())
    return data


def prepare_online_list(data):
    online_list = []
    directory_list = []

    # Iterate through all fetched galleries
    for g_index in data['galleries']:
        gallery = data['galleries'][g_index]
        title = gallery['title']

        # Add to directory list for all galleries
        directory_list.append(os.path.join(BASE_DIR, title))

        # Create directories for Galleries if they don't already exist
        if not os.path.exists(os.path.join(BASE_DIR, title)):
            os.makedirs(os.path.join(BASE_DIR, title))

        print title

        # Create list of tuples having (PHOTO_URL, DOWNLOAD_PATH)
        for p_index in gallery['photos']:
            photo = gallery['photos'][p_index]
            img_url = photo['url']
            url = urljoin(BASEURL, img_url)
            name = photo['name']
            online_list.append((url, os.path.join(BASE_DIR, title, name)))

    with open("config.json", "r") as jsonFile:
        config = json.load(jsonFile)

    config["directories"] = directory_list

    with open("config.json", "w") as jsonFile:
        json.dump(config, jsonFile, indent=2)
    return online_list


def prepare_existing_list(online_list):
    files_to_delete = []
    existing_files = []

    # Find all files inside Downloads/
    for (dirpath, dirnames, filenames) in os.walk(BASE_DIR):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            # Add files present to existing_files list
            existing_files.append(file_path)

            # If existing file doesn't exist in online list, delete
            found = False
            for online_file in online_list:
                if online_file[1] == file_path:
                    found = True
                    break
            if found is False:
                files_to_delete.append(file_path)

    return files_to_delete, existing_files


def download_files(online_list, existing_files):
    for file in online_list:
        if file[1] not in existing_files:
            urlretrieve(file[0], file[1])


def delete_files(files_to_delete):
    for file in files_to_delete:
        os.remove(file)


if __name__ == '__main__':
    data = fetch_data()

    print
    print("Script running at- " + str(datetime.datetime.now()))

    online_list = prepare_online_list(data)

    print
    print("Online List- " + str(len(online_list)))
    print(online_list)

    files_to_delete, existing_files = prepare_existing_list(online_list)

    print
    print("Existing Files- " + str(len(existing_files)))
    print(existing_files)

    print
    print("Files to delete- " + str(len(files_to_delete)))
    print(files_to_delete)

    download_files(online_list, existing_files)
    delete_files(files_to_delete)
