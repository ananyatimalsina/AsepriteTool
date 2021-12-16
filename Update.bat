set PATH=%PATH%;%CD%\Git\cmd\
git config --system http.sslcainfo %CD%\Git\mingw64\ssl\certs\ca-bundle.crt
cd C:\aseprite\
git pull
git submodule update --init --recursive