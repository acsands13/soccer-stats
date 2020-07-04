import logging
import json

from pathlib import Path

from soccer_stats.config import Config


class Scraper(object):
    def __init__(self, base_url, output_filename):
        Scraper.OUTPUT_PATH = '{}{}.json'.format(
            Config.DATA_PATH, output_filename)

    @classmethod
    def save(cls, results):
        logging.info('Saving {} total results to file.'.format(len(results)))
        output_path = '{}{}.json'.format(Config.DATA_PATH, cls.OUTPUT_FILENAME)
        with open(output_path, 'w') as fp:
            json.dump(results, fp)
        logging.info('Done.')

    @classmethod
    def load(cls):
        output_path = '{}{}.json'.format(Config.DATA_PATH, cls.OUTPUT_FILENAME)

        if not Path(output_path).exists():
            logging.info('No data file found. Running scraper...')
            cls.run()

        games = []
        with open(output_path, 'r') as fp:
            games = json.load(fp)
        return games

    @classmethod
    def run(cls):
        raise NotImplementedError
