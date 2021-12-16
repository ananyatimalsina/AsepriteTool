from pathlib import Path
from PIL import ImageTk
from tkinter import *
from tkinter import messagebox
import subprocess
import os
import zipfile

class MyOptionMenu(OptionMenu):
    def __init__(self, master, status, *options):
        self.var = StringVar(master)
        self.img = ImageTk.PhotoImage(file=relative_to_assets("button_1.png")) #replace with your own indicator image
        self.var.set(status)
        OptionMenu.__init__(self, master, self.var, *options)
        self.config(indicatoron=0, image = self.img, font=('calibri',(10)),bg='white',width=12)
        self['menu'].config(font=('calibri',(10)),bg='white')

class MyDialog:
    def __init__(self, parent, ttt):
        top = self.top = Toplevel(parent)
        top.geometry("200x100")
        self.myLabel = Label(top, text=ttt)
        self.myLabel.pack()

        self.myEntryBox = Entry(top)
        self.myEntryBox.pack()

        self.mySubmitButton = Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        global output
        output = self.myEntryBox.get()
        self.top.destroy()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
Mode = "Auto"

def Install():
    subprocess.call(["Install.bat"])

    skia_path_ins = MyDialog(window, ttt = "Path to Skia File")
    window.wait_window(skia_path_ins.top)
    skia_path = output
    ninja_path_ins = MyDialog(window, ttt = "Path to Ninja File")
    window.wait_window(ninja_path_ins.top)
    ninja_path = output

    try:
        with zipfile.ZipFile(skia_path, "r") as zf:
            zf.extractall("C:/deps/skia")

        with zipfile.ZipFile(ninja_path, "r") as zf:
            zf.extractall("C:/Program Files/CMake/bin")

    except Exception as e:
        messagebox.showerror("Unzip Error!", str(e))

    if os.path.isdir("C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/Tools"):
        subprocess.call(["Compile22.bat"])

    elif os.path.isdir("C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/Common7/Tools"):
        subprocess.call(["Compile19.bat"])

    else:
        messagebox.showerror("No Visual Studio installation found", "No Visual Studio installation found. Please refer to https://github.com/TheLiteCrafter/AsepriteTool")

    subprocess.call(["Shortcut.bat"])

def Update():
    subprocess.call(["Update.bat"])
    
    if os.path.isdir("C:/Program Files/Microsoft Visual Studio/2022/Community/Common7/Tools"):
        subprocess.call(["Compile22.bat"])

    elif os.path.isdir("C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/Common7/Tools"):
        subprocess.call(["Compile19.bat"])

    subprocess.call(["Shortcut.bat"])


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Start():
    if Mode == "Auto":

        if os.path.isdir("C:/aseprite") and os.path.isdir("C:\deps"):
            Update()

        else:
            Install()

    elif Mode == "Install":
        Install()

    elif Mode == "Update":
        Update()

def Help():
    messagebox.showinfo("Help", "Please Refer to https://github.com/TheLiteCrafter/AsepriteTool")


window = Tk()

window.geometry("700x800")
window.configure(bg = "#FFFFFF")
window.title("AsepriteTool")
window.iconbitmap("Icon.ico")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 800,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0000000000001,
    250.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = MyOptionMenu(window, Mode, "Install", "Update", "Auto")

button_1.place(
    x=35.000000000000114,
    y=723.0,
    width=170.0,
    height=60.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=Help,
    relief="flat"
)
button_2.place(
    x=495.0000000000001,
    y=723.0,
    width=170.0,
    height=60.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=Start,
    relief="flat"
)
button_3.place(
    x=265.0000000000001,
    y=723.0,
    width=170.0,
    height=60.0
)
window.resizable(False, False)
window.mainloop()