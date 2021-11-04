import os
import sys
import subprocess
import zipfile
import platform
import requests

first = True
command = "req"
InstallMode = "Auto"
Pre_Download = False

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
        print("InstallMode Auto/Update/Install - Changes the Installations-Mode")

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

                if platform.machine().endswith('64'):
                    subprocess.call(["Update64.bat"])

                else:
                    subprocess.call(["Update32.bat"])
            
                subprocess.call(["Compile.bat"])
                subprocess.call(["Shortcut.bat"])
            
            else:
                print("Install mode detected.")

                if platform.machine().endswith('64'):
                    subprocess.call(["Install64.bat"])

                else:
                    subprocess.call(["Install32.bat"])

                if Pre_Download == False:
                    skia_path = str(input("Please enter the path of the downloaded Skia.zip File: "))
                    ninja_path = str(input("Please enter the path of the downloaded Ninja.zip File: "))

                    try:
                        with zipfile.ZipFile(skia_path, "r") as zf:
                            zf.extractall("C:/deps/skia")

                        with zipfile.ZipFile(ninja_path, "r") as zf:
                            zf.extractall("C:/Program Files/CMake/bin")

                    except Exception as e:
                        print(e)

                else:

                    with zipfile.ZipFile("Skia.zip", "r") as zf:
                            zf.extractall("C:/deps/skia")

                    with zipfile.ZipFile("Ninja.zip", "r") as zf:
                        zf.extractall("C:/Program Files/CMake/bin")

                subprocess.call(["Compile.bat"])
                subprocess.call(["Shortcut.bat"])

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
        print("Skia - https://github.com/aseprite/skia/releases")
        print("")
        print("CMake - (https://cmake.org/download/) On Installer select Add to path for all Users")
        print("")
        print("Ninja - (https://github.com/ninja-build/ninja/releases)")
        print("")

        an = input("Do you want to automatically install all requierments? y/n: ")
        an = str(an).lower()

        if an == "y":

            Pre_Download = True

            with open("Cmake.msi", "wb") as code:
                code.write(requests.get("https://github.com/Kitware/CMake/releases/download/v3.22.0-rc2/cmake-3.22.0-rc2-windows-x86_64.msi").content)
                
                os.startfile("Cmake.msi")

            with open("VisualStudio.exe", "wb") as code:
                code.write(requests.get("https://aka.ms/vs/16/release/vs_community.exe").content)

                os.startfile("VisualStudio.exe")

            with open("Ninja.zip", "wb") as code:
                    code.write(requests.get("https://github.com/ninja-build/ninja/releases/download/v1.10.2/ninja-win.zip").content)

            if platform.machine().endswith('64'):
                with open("Skia.zip", "wb") as code:
                    code.write(requests.get("https://github.com/aseprite/skia/releases/download/m81-b607b32047/Skia-Windows-Release-x64.zip").content)

            else:
                with open("Skia.zip", "wb") as code:
                    code.write(requests.get("https://github.com/aseprite/skia/releases/download/m81-b607b32047/Skia-Windows-Release-x86.zip").content)

            print("Done!")

        elif an == "n":
            print("Allright! Make sure you have installed the requierments tho!")

        else:
            print("Invalid Answer!")

        first = False