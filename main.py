import requests
import telegram
from dotenv import load_dotenv
import os
import time

def run_bot(devman_token, telegram_token, chat_id):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': 'Token ' + devman_token}
    params = {'timestamp': ''}
    bot = telegram.Bot(token=telegram_token)
    while True:
        try:
            response = requests.get(url)
            response = requests.get(url, headers=headers, params=params, timeout=90)
            response.raise_for_status()
            response_decoded = response.json()
            if response_decoded['status'] == 'timeout':
                params['timestamp'] = response_decoded['timestamp_to_request']
            elif response_decoded['status'] == 'found':
                params['timestamp'] = response_decoded['last_attempt_timestamp']
                for attempt in response_decoded['new_attempts']:
                    message = f"The lesson \"{attempt['lesson_title']}\" has been assessed!"
                    if attempt['is_negative']:
                        message += ' Give it a one more try.'
                        bot.send_message(chat_id=chat_id, text=message)
                    else:
                        message += ' Everything is OK, go ahead!'
                        bot.send_message(chat_id=chat_id, text=message)
        except requests.exceptions.ReadTimeout:
            pass
        except ConnectionError:
            time.sleep(60)

def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    run_bot(devman_token, telegram_token, chat_id)

if __name__ == '__main__':
    main()



    
    
