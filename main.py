import requests
import telegram
from dotenv import load_dotenv
import os
import time
import logging


class LogsHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super(LogsHandler, self).__init__()
        self.token = token
        self.bot = telegram.Bot(token=self.token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def run_bot(devman_token, telegram_token, chat_id, logger):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': 'Token ' + devman_token}
    params = {'timestamp': ''}
    bot = telegram.Bot(token=telegram_token)
    logging.warning('The bot is running!')
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
        except Exception:
            logger.exception(Exception)


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    tg_logger_token = os.getenv('TG_LOGGER_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.WARNING)
    logger.addHandler(LogsHandler(tg_logger_token, chat_id))
    logger.warning("I'm Batman")

    run_bot(devman_token, telegram_token, chat_id, logger)


if __name__ == '__main__':
    main()



    
    
