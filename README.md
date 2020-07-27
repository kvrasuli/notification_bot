# Devman notification telegram bot

This is a telegram bot sending notifications about assessed lessons.

### How to use

You'll need you own Devman API token, Telegram API token and your chat ID.
Create 3 corresponding environment variables:
```
DEVMAN_TOKEN='your token'
TELEGRAM_TOKEN='your token'
CHAT_ID='your chat id'
```
Just run the python script main.py with the following concole command:
```
python main.py
```

### How to install dependencies

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
I don't think you need to use any virtual envs for such a small script.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).