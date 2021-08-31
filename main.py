import os
import sys
import subprocess
import zipfile

first = True
command = "req"

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

    elif command == "exit":
        sys.exit()

    elif command == "start":
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
            except Exception as e:
                print(e)

            try:
                with zipfile.ZipFile(ninja_path, "r") as zf:
                    zf.extractall("C:/Program Files/CMake/bin")
            except Exception as e:
                print(e)

            subprocess.call(["Compile.bat"])
            subprocess.call(["Shortcut.bat"])

    elif command == "req":
        print("Requierments: ")
        print("Visual Studio - (https://visualstudio.microsoft.com/) On the Installer select")
        print("Desktop Development with C++ and on Individual Items")
        print("(Check on Aseprites guide: https://github.com/aseprite/aseprite/blob/main/INSTALL.md under Windows dependencies)")
        print("")
        print("GitForWindows - (https://gitforwindows.org/) Leave evreything on Default.")
        print("")
        print("Skia - https://github.com/aseprite/skia/releases")
        print("")
        print("CMake - (https://cmake.org/download/) On Installer select Add to path for all Users")
        print("")
        print("Ninja - (https://github.com/ninja-build/ninja/releases) Unzip The File and Copy Ninja.exe to CmakeInstallLocation/bin")

        first = False