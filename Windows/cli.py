import os
import sys
from configparser import ConfigParser
import zipfile
import requests
from git import Repo
import subprocess

first = True
command = "req"
InstallMode = "Auto"

config = ConfigParser()

try:
    os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = os.getcwd() + "/Git/cmd"
    config.read("config.ini")
    vs_url = str(config["Settings"]["vs_link"])
    update = config["Settings"]["update"]
    git_url = config["Settings"]["git_link"]
    cmake_url = config["Settings"]["cmake_link"]
    skia_url = config["Settings"]["skia_link"]
    ninja_url = config["Settings"]["ninja_link"]
    n_p = config["Settings"]["ninja_path"]
    aseprite_path = config["Settings"]["aseprite_path"]

except Exception as e:
    print("Config File Is Corrupted or does not Exist!" + e)

if update == "True":

    if os.path.isdir("Git"):
        os.remove("Git")

    r_vs = requests.get(vs_url)
    r_git = requests.get(git_url)
    r_cmake = requests.get(cmake_url)
    r_skia = requests.get(skia_url)
    r_ninja = requests.get(ninja_url)

    os.mkdir("Git")

    open("Git.zip", "wb").write(r_git.content)
    open("vs.exe", "wb").write(r_vs.content)
    open("cmake.msi", "wb").write(r_cmake.content)
    open("skia.zip", "wb").write(r_skia.content)
    open("ninja.zip", "wb").write(r_ninja.content)

    with zipfile.ZipFile("Git.zip", "r") as zf:
        zf.extractall("Git")

    os.remove("Git.zip")

    os.system("cmake.msi")

    os.remove("cmake.msi")

    os.system("vs.exe")

    os.remove("vs.exe")

    config.set("Settings", "update", "False")

    with open("config.ini", "w") as configfile:
        config.write(configfile)

def change_install_mode(mode):
    InstallMode = mode
    print("Success! Install-Mode is now: " + InstallMode)

def Install():
    Repo.clone_from("https://github.com/aseprite/aseprite.git", aseprite_path + "aseprite", recursive = True)
    os.mkdir(aseprite_path + "deps")
    os.mkdir(aseprite_path + "aseprite/build")

    skia_path = "skia.zip"
    ninja_path = "ninja.zip"

    try:
        with zipfile.ZipFile(skia_path, "r") as zf:
            zf.extractall(aseprite_path + "deps/skia")

        with zipfile.ZipFile(ninja_path, "r") as zf:
            zf.extractall(n_p)

    except Exception as e:
        print(e)

    if os.path.isdir("C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/Tools"):
        _extracted_from_Install_21(
            'call "C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    elif os.path.isdir("C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/Common7/Tools"):
        _extracted_from_Install_21(
            'call "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    else:
        print("No Visual Studio installation found", "No Visual Studio installation found. Please refer to https://github.com/TheLiteCrafter/AsepriteTool")

    os.system('shortcut /a:c /f:"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Aseprite.lnk" /t:"' + aseprite_path + 'build/bin/aseprite.exe"')

    print("Done! Finisched Compiling Aseprite! It can be found by searching for aseprite in the start menu")
    os.remove("cmd.bat")

# TODO Rename this here and in `Install`
def _extracted_from_Install_21(arg0):
    with open("cmd.bat", "w") as f:
        f.write(arg0 + "\n")
        f.write("cd " + aseprite_path + "aseprite" + "\n")
        f.write("mkdir build" + "\n")
        f.write("cd build" + "\n")
        f.write("cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLAF_BACKEND=skia -DSKIA_DIR=" + aseprite_path + "deps/skia" + " -DSKIA_LIBRARY_DIR=" + aseprite_path + "deps/skia/out/Release-x64" + " -DSKIA_LIBRARY=" + aseprite_path + "deps/skia/out/Release-x64/skia.lib" + " -G Ninja .." + "\n")
        f.write("ninja aseprite")

    subprocess.call(["cmd.bat"])

def Update():
    repo = Repo(aseprite_path + "aseprite")
    o = repo.remotes.origin
    o.pull()

    for submodule in repo.submodules:
        submodule.update(init=True, recursive=True)

    if os.path.isdir("C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/Tools"):
        _extracted_from_Update_8(
            'call "C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    elif os.path.isdir("C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/Common7/Tools"):
        _extracted_from_Update_8(
            'call "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    else:
        print("No Visual Studio installation found", "No Visual Studio installation found. Please refer to https://github.com/TheLiteCrafter/AsepriteTool")

    os.system('shortcut /a:c /f:"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Aseprite.lnk" /t:"' + aseprite_path + 'build/bin/aseprite.exe"')

    print("Done! Finisched Compiling Aseprite! It can be found by searching for aseprite in the start menu")
    os.remove("cmd.bat")

# TODO Rename this here and in `Update`
def _extracted_from_Update_8(arg0):
    with open("cmd.bat", "w") as f:
        f.write(arg0 + "\n")
        f.write("cd " + aseprite_path + "aseprite/build" + "\n")
        f.write("cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLAF_BACKEND=skia -DSKIA_DIR=C:\deps\skia -DSKIA_LIBRARY_DIR=C:\deps\skia\out\Release-x64 -DSKIA_LIBRARY=C:\deps\skia\out\Release-x64\skia.lib -G Ninja .." + "\n")
        #f.write("cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLAF_BACKEND=skia -DSKIA_DIR=" + aseprite_path + "deps/skia" + " -DSKIA_LIBRARY_DIR=" + aseprite_path + "deps/skia/out/Release-x64" + " -DSKIA_LIBRARY=" + aseprite_path + "deps/skia/out/Release-x64/skia.lib" + " -G Ninja .." + "\n")
        f.write("ninja aseprite")

    subprocess.call(["cmd.bat"])

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

            if os.path.isdir(aseprite_path + "aseprite") and os.path.isdir(aseprite_path + "deps"):
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
        print("Visual Studio and Cmake will automatically be downloaded. On Cmake dont forget to select add to Path for all Users, and on Visual Studio the Desktop Development with C++ and under Individual Items (Check on Aseprite Guide: https://github.com/aseprite/aseprite/blob/main/INSTALL.md#windows-dependencies)")

        first = False