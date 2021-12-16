set PATH=%PATH%;%CD%\Git\cmd\
git config --system http.sslcainfo %CD%\Git\mingw64\ssl\certs\ca-bundle.crt
cd C:\
git clone --recursive https://github.com/aseprite/aseprite.git
mkdir deps
mkdir skia