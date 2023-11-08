import os
import shutil
import requests
import re

def removeFolder(directory):
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass

removeFolder("./app/src/main/python")
os.mkdir("./app/src/main/python")

version = re.search("VERSION = '\d+\.\d+\.\d+'", requests.get("https://raw.githubusercontent.com/BetterLectio/python-lectio/main/setup.py").text).group().split("'")[1]
open("version.txt", "w").write(version)

requirements = requests.get("https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/requirements.txt").text
open("./app/src/main/python/requirements.txt", "w").write(requirements)


app = requests.get("https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/api/app.py").text
app = app.replace("if __name__ == '__main__':\n    app.run()", "")
app += f"""
@app.route("/app_version")
def app_version():
    return \"{version}\"

from threading import Thread

def thread():
    app.run(host="0.0.0.0")

def main():
    Thread(target=thread).start()
"""
open("./app/src/main/python/app.py", "w").write(app)

oldGradleProperties = open("./gradle.properties").read()
open("./gradle.properties", "a").write(f"""
# APK signing
RELEASE_STORE_FILE=../keystore/key.jks
RELEASE_STORE_PASSWORD={os.environ["RELEASE_STORE_PASSWORD"]}
RELEASE_KEY_ALIAS={os.environ["RELEASE_KEY_ALIAS"]}
RELEASE_KEY_PASSWORD={os.environ["RELEASE_KEY_PASSWORD"]}
""") #RELEASE_KEY_ALIAS={os.environ["RELEASE_KEY_ALIAS"]}

removeFolder("./app/build/outputs/apk/")
os.system("./gradlew build")

open("./gradle.properties", "w").write(oldGradleProperties)

removeFolder("dist")
os.mkdir("dist")
shutil.move("./app/build/outputs/apk/release/app-release.apk", "./dist/betterlectio.apk")

print("APK with updated backend can be found at ./dist/betterlectio.apk")
