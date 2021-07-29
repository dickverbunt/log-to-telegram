#!/usr/bin/python3

import subprocess
import yaml
import requests
import time
import logging

# Setup logging
logging.basicConfig(filename='debug.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

timeout_time = 0;

def sendTelegramMessage(message):
    print('Sending Telegram: ' + message)
    logging.debug('Sending Telegram: ' + message)

    bot_token = config['telegram']['bot_token']
    bot_chatID = config['telegram']['bot_chatID']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)

# Load config file
with open("config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Connect to file
f = subprocess.Popen(['tail','-F','file.log'],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)

logging.debug('Running')
logging.debug('Loaded config: ' + str(config))

# Main loop
while True:
    line = str(f.stdout.readline())

    # Check timeout
    time_start = time.time()
    time_elapsed = round(time_start - timeout_time)
    if time_elapsed > config['timeout']:
        # Check all triggers
        for trigger in config['triggers']:
            if trigger in line:
                # Reset timeout
                timeout_time = time_start

                # Send telegram message
                sendTelegramMessage(line);
    else:
        logging.debug(f'Timeout (time elapsed: {time_elapsed} seconds)')
        print(f'Timeout (time elapsed: {time_elapsed} seconds)');
