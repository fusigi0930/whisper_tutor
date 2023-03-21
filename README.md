this project makes human talk with ChatGPT, and running in windows/ubuntu system. \
it uses chatgpt-3.5-turbo model, before you use it, please generate a secret key \
from openai official website. \
\
**notice: chatgpt-3.5-turbo needs charge, 0.002 USD/1000 tokens about 750 words** \
**the words contain both of you and chatGPT response** 

# initial environment

## Linux

```shell
# python 3.9
sudo apt install python3.9
sudo apt install python3-testresources ffmpeg
sudo apt install libpython3.9-dev portaudio19-dev pavucontrol espeak libmpv-dev git git-lfs
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

git lfs install
python -m venv env
source env/bin/activate
pip install -r requirements_linux.txt
```

## Windows

in windows, it need install python3.9, ffmpeg, espeak, visual studio 2022 community and you can find this on the following web site \
ffmpeg: https://www.gyan.dev/ffmpeg/builds/ \
python3.9: https://www.python.org/ftp/python/3.9.9/python-3.9.9-amd64.exe \
espeak: https://espeak.sourceforge.net/download.html \
visual studio 2022 community: https://visualstudio.microsoft.com/zh-hant/vs/community/ \
wsl or git environment with git-lfs installed
\
**notice: ffmpeg and espeak have to add into the PATH variable**

```batch
python.exe -m venv env
call env/script/activate.bat
pip install -r requirements_win.txt
copy lib\win\mpv-2.dll env\Script\

```

# set the openai API
you need create a openai account and create a secret key by yourself in this url
https://platform.openai.com/account/api-keys

copy your key into a file "config.py" with global variable chatgpt_key.
e.g.
```python
chatgpt_key = "<your key>"
```

# run the tutor

## Linux
```shell
source env/bin/activate
python tutor_en.py 2>/dev/null
```

## Windows
```
call env/script/activate.bat
python tutor_en.py
```
use this command, that contains speech recognize, tts in local side and use chatGPT 3.5 api to get a chat robot response.
