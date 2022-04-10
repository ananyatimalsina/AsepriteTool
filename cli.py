import os
import sys
from configparser import ConfigParser
import zipfile
import requests
import subprocess
import shutil
from requests_html import HTML

first = True
command = "req"
InstallMode = "Auto"

config = ConfigParser()

try:
    config.read("config.ini")
    vs_url = str(config["Settings"]["vs_link"])
    update = config["Settings"]["update"]
    skia_url = config["Settings"]["skia_link"]
    ninja_url = config["Settings"]["ninja_link"]
    n_p = config["Settings"]["ninja_path"]
    p_path = config["Settings"]["p_path"]
    aseprite_path = config["Settings"]["aseprite_path"]
    aseprite_link = config["Settings"]["aseprite_link"]

except Exception as e:
    print("Config File Is Corrupted or does not Exist!" + e)

if update == "True":
    if os.path.isdir("Git"):
        shutil.rmtree("Git")

    git_r = requests.get("https://github.com/git-for-windows/git/releases/")
    git_r = HTML(html=str(git_r.content))
    git_url = git_r.links
    for i in git_url:
        if "MinGit" in i:
            git_url = i
            break

    cmake_r = requests.get("https://cmake.org/download/")
    cmake_r = HTML(html=str(cmake_r.content))
    cmake_url = cmake_r.links
    for i in cmake_url:
        if "windows" in i and "msi" in i:
            cmake_url = i
            break

    git_url = "https://github.com" + git_url

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
    with open("Install.bat", "w") as f:
        f.write("SET PATH=%PATH%;" + os.getcwd() + "/Git/cmd" + "\n")
        f.write("cd " + aseprite_path + "\n")
        f.write("git clone --recursive " + aseprite_link)

    subprocess.call(["Install.bat"])

    os.remove("Install.bat")

    skia_path = "skia.zip"
    ninja_path = "ninja.zip"

    try:
        with zipfile.ZipFile(skia_path, "r") as zf:
            zf.extractall(aseprite_path + "deps/skia")

        with zipfile.ZipFile(ninja_path, "r") as zf:
            zf.extractall(n_p)

    except Exception as e:
        print(e)

    if os.path.isdir(p_path + "Microsoft Visual Studio/2022/Community/Common7/Tools"):
        _extracted_from_Install_21(
            'call "' + p_path + 'Microsoft Visual Studio/2022/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    elif os.path.isdir(p_path + " (x86)" + "/Microsoft Visual Studio/2019/Community/Common7/Tools"):
        _extracted_from_Install_21(
            'call "' + p_path + ' (x86)' + '/Microsoft Visual Studio/2019/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    else:
        print("No Visual Studio installation found", "No Visual Studio installation found. Please refer to https://github.com/TheLiteCrafter/AsepriteTool")

    os.system('shortcut /a:c /f:"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Aseprite.lnk" /t:"' + aseprite_path + 'aseprite/build/bin/aseprite.exe"')

    print("Done! Finished Compiling Aseprite! It can be found by searching for aseprite in the start menu")
    os.remove("cmd.bat")

# TODO Rename this here and in `Install`
def _extracted_from_Install_21(arg0):
    with open("cmd.bat", "w") as f:
        f.write(arg0 + "\n")
        f.write("cd " + aseprite_path + "aseprite" + "\n")
        f.write("mkdir build" + "\n")
        f.write("cd " + aseprite_path + "aseprite/build" + "\n")
        f.write("cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLAF_BACKEND=skia -DSKIA_DIR=" + aseprite_path + "deps/skia" + " -DSKIA_LIBRARY_DIR=" + aseprite_path + "deps/skia/out/Release-x64" + " -DSKIA_LIBRARY=" + aseprite_path + "deps/skia/out/Release-x64/skia.lib" + " -G Ninja .." + "\n")
        f.write("ninja aseprite")

    subprocess.call(["cmd.bat"])

def Update():
    with open("cmd.bat", "w") as f:
        f.write("SET PATH=%PATH%;" + os.getcwd() + "/Git/cmd" + "\n")
        f.write("cd " + aseprite_path + "aseprite" + "\n")
        f.write("git pull" + "\n")
        f.write("git submodule update --init --recursive")

    if os.path.isdir(p_path + "Microsoft Visual Studio/2022/Community/Common7/Tools"):
        _extracted_from_Install_21(
            'call "' + p_path + 'Microsoft Visual Studio/2022/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    elif os.path.isdir(p_path + " (x86)" + "/Microsoft Visual Studio/2019/Community/Common7/Tools"):
        _extracted_from_Install_21(
            'call "' + p_path + ' (x86)' + '/Microsoft Visual Studio/2019/Community/Common7/Tools/VsDevCmd.bat" -arch=x64'
        )

    else:
        print("No Visual Studio installation found", "No Visual Studio installation found. Please refer to https://github.com/TheLiteCrafter/AsepriteTool")

    os.system('shortcut /a:c /f:"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Aseprite.lnk" /t:"' + aseprite_path + 'aseprite/build/bin/aseprite.exe"')

    print("Done! Finished Compiling Aseprite! It can be found by searching for aseprite in the start menu")
    os.remove("cmd.bat")

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
        r = requests.get("https://github.com/aseprite/aseprite/blob/main/INSTALL.md#windows-dependencies")
        sdk = str(r.content).split('Desktop development with C++ item + ', 1)[1]
        sdk = sdk[:sdk.find('</a>')]

        print("Requierments: ")
        print("")
        print("Visual Studio and Cmake will automatically be downloaded. On Cmake dont forget to select add to Path for all Users, and on Visual Studio the Desktop Development with C++ and under Individual Items " + sdk)

        first = False