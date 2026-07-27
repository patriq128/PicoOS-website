import urequests #type: ignore
from system.apps import install
import ujson #type: ignore
import hashlib
import os
import sys
from system.apps import install
from shell.commands import cd, rm

def hash_count(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(512)
            if not chunk:
                break
            h.update(chunk)

    return ''.join('{:02x}'.format(b) for b in h.digest())


def apps(command, app):
    if command != "install":
        return

    manifest = urequests.get(
        "https://picoos.dev/download/apps/manifest.json"
    )

    if manifest.status_code != 200:
        print("Manifest download failed")
        return

    data = manifest.json()
    manifest.close()
    try:
        with open("/conf/apps.conf") as f:
            conf = ujson.load(f)

        exist = conf.get(app, False)
    except Exception:
        exist = False

    filename = f"{app}.pcs"

    if filename not in data:
        print("App not exist")
        return

    if exist == data[filename]:
        print("Already the newest version.")
        return

    print(f"Installing \033[32m{app}\033[0m")
    get_file = urequests.get(
        f"https://picoos.dev/download/apps/{filename}"
    )

    if get_file.status_code == 200:
        with open(f"/{app}.pcs", "wb") as f:
            while True:
                chunk = get_file.raw.read(512)
                if not chunk:
                    break

                f.write(chunk)

        get_file.close()
        install(app)
        rm(filename)
    else:
        print("Download failed")

def update():
    update = []
    manifest = urequests.get("https://picoos.dev/download/system/manifest.json")
    data = manifest.json()

    for file in data.keys():

        try:
            current_hash = hash_count("/" + file)

            if current_hash != data[file]:
                update.append(file)

        except OSError:
            print("Missing file:", file)

    if update:
        print("Files to update / install:")
        for code in update:
            print("\033[32m", code)
        respond = input("\033[0mContinue ? [Y/n]: \033[0m")
        if respond == "y":
            for code in update:
                print(f"Downloading\033[32m {code}\033[0m")
                get_file = urequests.get(f"https://picoos.dev/download/system/{code}")
                data = get_file.text
                with open(f"/{code}", "w") as f:
                    f.write(data)
            print("\033[32m Done :)\033[0m")
            get_file.close()
    else:
        print("There is nothing to do")
        print("Everything is upadted :3")
    manifest.close()
