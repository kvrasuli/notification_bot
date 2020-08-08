import requests
import telegram
from dotenv import load_dotenv
import os
import time
import logging
import sys
import traceback as tb


logger = logging.getLogger('Batman')


class LogsHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.bot = telegram.Bot(token=self.token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def run_bot(devman_token, telegram_token, chat_id, logger):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {devman_token}'}
    params = {'timestamp': ''}
    bot = telegram.Bot(token=telegram_token)
    logger.info('The bot is running!')
    while True:
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=90
            )
            response.raise_for_status()
            dvmn_response = response.json()
            if dvmn_response['status'] == 'timeout':
                params['timestamp'] = dvmn_response['timestamp_to_request']
            elif dvmn_response['status'] == 'found':
                params['timestamp'] = dvmn_response['last_attempt_timestamp']
                for attempt in dvmn_response['new_attempts']:
                    message = f"The lesson \"{attempt['lesson_title']}\" \
                                has been assessed!"
                    if attempt['is_negative']:
                        message += ' Give it a one more try.'
                        bot.send_message(chat_id=chat_id, text=message)
                    else:
                        message += ' Everything is OK, go ahead!'
                        bot.send_message(chat_id=chat_id, text=message)
        except requests.exceptions.ReadTimeout:
            pass
        except ConnectionError:
            logger.exception('Connection error!')
            tb.print_exc()
            time.sleep(60)
        except Exception:
            logger.exception('Error!')
            tb.print_exc()
            sys.exit()


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    tg_logger_token = os.getenv('TG_LOGGER_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(tg_logger_token, tg_chat_id))
    logger.info("I'm Batman")

    run_bot(devman_token, telegram_token, tg_chat_id, logger)


if __name__ == '__main__':
    main()
