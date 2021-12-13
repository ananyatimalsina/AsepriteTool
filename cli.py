import os
import sys
import subprocess
import zipfile
import platform
import requests

first = True
command = "req"
InstallMode = "Auto"

def change_install_mode(mode):
    InstallMode = mode
    print("Success! Install-Mode is now: " + InstallMode)


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

            if os.path.isdir("C:/aseprite") and os.path.isdir("C:\deps"):
                print("Update Mode detected.")

                subprocess.call(["Update.bat"])
                subprocess.call(["Compile.bat"])
                subprocess.call(["Shortcut.bat"])
            
            else:
                print("Install mode detected.")

                subprocess.call(["Install.bat"])

                skia_path = str(input("Please enter the path of the downloaded Skia.zip File: "))
                ninja_path = str(input("Please enter the path of the downloaded Ninja.zip File: "))

                try:
                    with zipfile.ZipFile(skia_path, "r") as zf:
                        zf.extractall("C:/deps/skia")

                    with zipfile.ZipFile(ninja_path, "r") as zf:
                        zf.extractall("C:/Program Files/CMake/bin")

                except Exception as e:
                    print(e)

        elif InstallMode == "Install":
            print("Install mode Selected.")
            subprocess.call(["Install.bat"])
            skia_path = str(input("Please enter the path of the downloaded Skia.zip File: "))
            ninja_path = str(input("Please enter the path of the downloaded Ninja.zip File: "))

            try:
                with zipfile.ZipFile(skia_path, "r") as zf:
                    zf.extractall("C:/deps/skia")

            except Exception as e:
                print(e)

            try:
                with zipfile.ZipFile(ninja_path, "r") as zf:
                    zf.extractall("C:/Program Files/CMake/bin")
            except Exception as e:
                print(e)

            subprocess.call(["Compile.bat"])
            subprocess.call(["Shortcut.bat"])

        elif InstallMode == "Update":
            print("Update Mode detected.")
            subprocess.call(["Update.bat"])
            subprocess.call(["Compile.bat"])
            subprocess.call(["Shortcut.bat"])

    elif command == "req":
        print("Requierments: ")
        print("Visual Studio - (https://visualstudio.microsoft.com/) On the Installer select")
        print("Desktop Development with C++ and on Individual Items")
        print("(Check on Aseprites guide: https://github.com/aseprite/aseprite/blob/main/INSTALL.md under Windows dependencies)")
        print("")
        print("Git - https://git-scm.com/download/win Check Add to Path")
        print("")
        print("CMake - (https://cmake.org/download/) On Installer select Add to path for all Users")
        print("")
        print("Skia - https://github.com/aseprite/skia/releases")
        print("")
        print("Ninja - (https://github.com/ninja-build/ninja/releases)")
        print("")

        first = False