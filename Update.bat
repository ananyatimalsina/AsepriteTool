set PATH=%PATH%;%CD%\Git\cmd\
git config --system http.sslverify false
cd C:\aseprite\
git pull
git submodule update --init --recursive