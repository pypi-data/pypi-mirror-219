'''
last editted: 2023-07-18
version: 0.4.0
'''
from main_logic import start
import logging
from configparser import ConfigParser

def main():
    # config = ConfigParser()
    # config.read("./market_place_cli/config/log.config", encoding="UTF-8")
    # logging.basicConfig(filename=f'{config["log"]["log_dir"]}{config["log"]["filename"]}',
    #                     level=logging.DEBUG,
    #                     format=config["log"]["LOG_FORMAT"],
    #                     datefmt=config["log"]["DATE_FORMAT"],
    #                     )
    start()

if __name__ == '__main__':
    main()
