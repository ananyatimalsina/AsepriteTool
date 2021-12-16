set PATH=%PATH%;%CD%\Git\cmd\
git config --system http.sslverify false
cd C:\
git clone --recursive https://github.com/aseprite/aseprite.git
mkdir deps
mkdir skia