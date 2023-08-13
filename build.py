import os
import shutil
import requests

def removeFolder(directory):
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass


removeFolder("./app/src/main/python")
os.mkdir("./app/src/main/python")

package = requests.get("https://raw.githubusercontent.com/BetterLectio/betterLectio/main/package.json").json()
app = requests.get("https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/api/app.py").text
app = app.replace("if __name__ == '__main__':\n    app.run()", "")
app += f"""
@app.route("/app_version")
def app_version():
    return "{package["version"]}"

from threading import Thread

def thread():
    app.run(host="0.0.0.0")

def main():
    Thread(target=thread).start()
"""
open("./app/src/main/python/app.py", "w").write(app)

requirements = requests.get("https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/requirements.txt").text
open("./app/src/main/python/requirements.txt", "w").write(requirements)

# keystore path = /home/jonathan/Skrivebord/BetterLectio/BetterLectioMobile/keystore/key.jks
# keystore password: f("=Su(("!=?)#"!93:_

"""
Key:
    Alias: key0
    Password: gi)#"(#jSNAbvB5!
    Validity: 25 years
    Certificate:
        First and Last Name: BetterLectio Mobile
        Organizational Unit: BetterLectio
        Organizational: BetterLectio
        City or Locality: Kongens Lyngby
        State or Province: Storkøbenhavn
        Country Code (XX): 45
"""

oldGradleProperties = open("./gradle.properties").read()
open("./gradle.properties", "a").write(f"""
# APK signing
RELEASE_STORE_FILE=../keystore/key.jks
RELEASE_STORE_PASSWORD={os.environ["RELEASE_STORE_PASSWORD"]}
RELEASE_KEY_ALIAS={os.environ["RELEASE_KEY_ALIAS"]}
RELEASE_KEY_PASSWORD={os.environ["RELEASE_KEY_PASSWORD"]}
""")

shutil.rmtree("./app/build/outputs/apk/")
os.system("./gradlew build")

open("./gradle.properties", "w").write(oldGradleProperties)

shutil.rmtree("dist")
os.mkdir("dist")
shutil.move("./app/build/outputs/apk/release/app-release.apk", "./dist/betterlectio.apk")

print("APK with updated backend can be found at ./dist/betterlectio.apk")