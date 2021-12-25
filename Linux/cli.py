import os
import sys
import subprocess
from configparser import ConfigParser
import zipfile

first = True
command = "req"
InstallMode = "Auto"

config = ConfigParser()

try:
    config.read("config.ini")
    update = config["Settings"]["update"]

except Exception as e:
    print("Config File Is Corrupted or does not Exist!")
    sys.exit("Config File Is Corrupted or does not Exist!")

if update == "True":

    subprocess.call(["Dependencies.sh"])

    config.set("Settings", "update", "False")

    with open("config.ini", "w") as configfile:
        config.write(configfile)

def change_install_mode(mode):
    InstallMode = mode
    print("Success! Install-Mode is now: " + InstallMode)

def Install():
    subprocess.call(["Install.sh"])

    skia_path = str(input("Please enter the path of the downloaded Skia.zip File: "))

    try:
        with zipfile.ZipFile(skia_path, "r") as zf:
            zf.extractall(os.path.expanduser("~")+"/deps/skia")

    except Exception as e:
        print(str(e))

    subprocess.call(["Compile.sh"])

    print("Done! Finisched Compiling Aseprite! It can be found in $HOME/aseprite/bin")

def Update():
    subprocess.call(["Update.sh"])

    subprocess.call(["Compile.bat"])

    print("Done! Finisched Compiling Aseprite! It can be found in $HOME/aseprite/bin")

while 1:
    if first == False:
        command = input("Please Enter a Command: ")
        command = str(command).lower()

    if command == "help":
        print("List of avilable commands:")
        print("help - Shows a List of all avilable commands")
        print("start - Starts the install/update process")
        print("exit - Exists the programm")
        print("req - Shows all requierments")
        print("InstallMode Auto/Update/Install - Changes the Installation-Mode")

    elif command == "installmode auto":
        change_install_mode("Auto")

    elif command == "installmode install":
        change_install_mode("Install")
    
    elif command == "installmode update":
        change_install_mode("Update")

    elif command == "exit":
        sys.exit()

    elif command == "start":

        if InstallMode == "Auto":

            if os.path.isdir(os.path.expanduser("~")+"/aseprite") and os.path.isdir(os.path.expanduser("~")+"/deps"):
                print("Update Mode detected.")

                Update()
            
            else:
                print("Install mode detected.")

                Install()

        elif InstallMode == "Install":
            Install()

        elif InstallMode == "Update":
            Update()

    elif command == "req":
        print("Requierments: ")
        print("")
        print("Skia - https://github.com/aseprite/skia/releases")
        print("")

        first = False