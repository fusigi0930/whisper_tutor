
# initial environment
```shell
# python 3.9 (and later)
sudo apt install python3.9
sudo apt install python3-testresources ffmpeg
sudo apt install libpython3.9-dev portaudio19-dev pavucontrol espeak
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
# set the openai API
you need create a openai account and create a secret key by yourself in this url
https://platform.openai.com/account/api-keys

copy your key into a file "config.py" with global variable chatgpt_key.
e.g.
```python
chatgpt_key = <your key>
```

# run the tutor
```shell
python tutor_en.py 2>/dev/null
```
use this command, that contains speech recognize, tts in local side and use chatGPT 3.5 api to get a chat robot response.
