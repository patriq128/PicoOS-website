# FIXME
# - Installing error

import urequests
from system.apps import install
import ujson
import hashlib
import os

class Apps:
    def install(self, app):
        url = f"https://picoos.dev/download/apps/{app}.py"

        try:
            response = urequests.get(url)

            if response.status_code == 200:
                print(f"Installing {app}")
                data = response.text
                with open(f"/{app}.py", "w") as f:
                    f.write(data)

            elif response.status_code == 404:
                print(f"App {app} not existing")

            response.close()

        except Exception as e:
            print(e)

apps = Apps()

BASE_URL = "https://picoos.dev/downloads/system/"


def get_hash(path):
    try:
        with open(path, "rb") as f:
            data = f.read()

        return hashlib.sha256(data).hexdigest()

    except:
        return None


def download_file(path):
    url = BASE_URL + path
    print("Downloading:", path)
    r = urequests.get(url)
    if r.status_code == 200:
        folder = path.rsplit("/", 1)[0]

        try:
            os.mkdir(folder)
        except:
            pass

        with open("/" + path, "wb") as f:
            f.write(r.content)

        print("Updated:", path)
    else:
        print("Failed:", path)
    r.close()

def update():
    print("Checking updates...")
    r = urequests.get(BASE_URL + "manifest.json")
    manifest = r.json()
    r.close()
    for file, remote_hash in manifest.items():
        local_hash = get_hash("/" + file)
        if local_hash != remote_hash:
            print("Change detected:", file)
            download_file(file)
        else:
            print("OK:", file)