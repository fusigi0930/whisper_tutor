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

# in whisper_tutor
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
rem in whisper_tutor

python.exe -m venv env
call env/script/activate.bat
pip install -r requirements_win.txt
copy lib\win\mpv-2.dll env\Script\

```

# set chat engine

## set the openai API
if you want to use the chatgpt-3.5 to your chat engine, you need create a openai account and create a secret key by yourself in this url
https://platform.openai.com/account/api-keys

copy your key into a file "config.py" with global variable chatgpt_key.
e.g.
```python
chatgpt_key = "<your key>"
```

## set the EdgeGPT cookies
or you can try this chat engine "edgegpt" that is based on the web communication to "bing.com", at the frist, you need refer the document
"https://github.com/acheong08/EdgeGPT/tree/master/docs#getting-authentication-required", and copy the cookie json file to "bing-cookies.json"
after that, we can use the edgegpt engine.

# run

## tutor
use this command, that contains speech recognize, tts in local side and use chatGPT 3.5 api to get a chat robot response.

the following are command arguments \
-s, -speed: (optional) the TTS speed usually fast, use 0.91 multiple speed will clearly \
-f, --file: (optional) set the log file name, default uses the date information to filename \
-e, --engine: (optional) set the chat engine, default value is "bingchat" \
             the value should be "chatgpt" or "bingchat", otherwise will set to "bingchat"


### Linux
```shell
source env/bin/activate
python tutor_en.py --speed 0.91 -file <logname> 2>/dev/null
```

### Windows
```
call env/script/activate.bat
python tutor_en.py --speed 0.91 -file <logname>
```

## reader
it only read the log file from tutor (actully, it can read nomral texts) with chatGPT api (so, no charge)

the following are command arguments
speed: (optional) the TTS speed usually fast, use 0.91 multiple speed will clearly
file: read filename

### Linux
```shell
source env/bin/activate
python read_en.py -f <file> -s 0.91 2>/dev/null
```

### Windows
```
call env/script/activate.bat
python read_en.py -f <file> -s 0.91
```