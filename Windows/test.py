import requests

url = requests.get("https://github.com/aseprite/skia/releases/latest/download/Skia-Windows-Release-x64.zip")

open("test.zip", "wb").write(url.content)