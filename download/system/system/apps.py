import json
import os
from shell.commands import touch, cd, rm
from kernel.colors import colors
from kernel.debug import debug
from system.pcs import pcs
import hashlib
import sys

def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            data = f.read(512)
            if not data:
                break
            h.update(data)

    return "".join("{:02x}".format(b) for b in h.digest())

class Apps:

    def load(self):
        try:
            with open("/conf/apps.conf", "r") as f:
                return json.load(f)
        except Exception:
            touch("/conf/apps.conf")
            return {}

    def save(self, app):
        data = self.load()
        data.update(app)

        with open("/conf/apps.conf", "w") as f:
            json.dump(data, f)

    def run(self, app, args=None):
        if args is None:
            args = []
        elif not isinstance(args, (list, tuple)):
            args = [args]

        try:
            module_name = "apps." + app + ".main"

            mod = __import__(module_name)

            for part in module_name.split(".")[1:]:
                mod = getattr(mod, part)

        except Exception as e:
            print("Error loading app:", e)
            debug.error("Error loading app", str(e))
            return

        try:
            mod.main(*args)
        except Exception as e:
            print("Error running app:", e)
            debug.error("Error running app", str(e))


apps = Apps()


def install(app):
    try:
        file_hash = sha256_file(f"{app}.pcs")
        try:
            with open("/conf/apps.conf", "r") as f:
                data = json.load(f)
        except:
            data = {}

        if app in data:
            if data[app]["Hash"] == file_hash:
                print("Already the newest version")
                return
            else:
                print("Updating")
        else:
            print("Installing")

        pcs(f"{app}.pcs")

        with open(f"/apps/{app}/manifest.json", "r") as f:
            info = json.load(f)

        data[app] = {
            "Version": info["version"],
            "Autor": info["autor"],
            "Hash": file_hash
        }

        apps.save(data)

    except Exception as e:
        print("Something went wrong:", e)
        debug.error("Error installing app", str(e))

def online_install(app):
    import urequests #type: ignore
    import ujson #type: ignore
    manifest = urequests.get("https://picoos.dev/download/apps/manifest.json")

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

class Apps_manager:
    def install(self, read):
        result = sys.implementation._machine
        if "Pico W" in result:
            W = True
        else:
            W = False
        if not read.endswitch(".pcs"):
            if W:
                import urequests #type: ignore
                manifest = urequests.get("https://picoos.dev/download/system/manifest.json")
                data = manifest.json()
                if read in data.keys():
                    online_install(read)
                else:
                    try:
                        os.stat(f"{read}.pcs")
                    except:
                        print("The app is not existing")
            else:
                try:
                    os.stat(f"{read}.pcs")
                except:
                    print("The app is not existing")
        else:
             install(read)
        

    def main(self, arg, arg1=None):
        if arg == "list":
            data = apps.load()
            print("Installed apps:")
            for i in data.keys():
                print(i)
        if arg == "install":
            self.install(arg1)

apps_manager = Apps_manager()