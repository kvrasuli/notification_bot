import requests
import telegram
from dotenv import load_dotenv
import os

def run_bot(devman_token, telegram_token, chat_id):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': 'Token ' + devman_token}
    params = {'timestamp': ''}
    bot = telegram.Bot(token=telegram_token)
    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=120)
            if response.json()['status'] == 'timeout':
                params['timestamp'] = response.json()['timestamp_to_request']
            elif response.json()['status'] == 'found':
                for attempt in response.json()['new_attempts']:
                    message = f"The lesson \"{attempt['lesson_title']}\" has been assessed!"
                    if attempt['is_negative']:
                        message += 'Give it a one more try.'
                        bot.send_message(chat_id=chat_id, text=message)
                    else:
                        message += 'Everything is OK, go ahead!'
                        bot.send_message(chat_id=chat_id, text=message)
        except requests.exceptions.ReadTimeout:
            print('Timeout!')
        except ConnectionError:
            print('Connection error.')

if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    run_bot(devman_token, telegram_token, chat_id)


    
    
