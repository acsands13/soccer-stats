import logging
import re
import requests

from bs4 import BeautifulSoup

from soccer_stats.scraping import Scraper


class FIFA(Scraper):
    LEAGUE_NAME = 'FIFA World Cup'
    BASE_URL = 'https://www.fifa.com'
    OUTPUT_FILENAME = 'fifa_world_cup'

    @classmethod
    def _get_years(cls):
        url = '{}/fifa-tournaments/archive/worldcup/index.html'.format(
            cls.BASE_URL)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        years = soup.select('li.comp-item a.link-wrap')
        ids = []
        for a in years:
            href = a['href'].strip()
            result = re.search(
                '/worldcup/archive/(.*)/index.html', href)
            ids.append(result.group(1))
        return ids

    @classmethod
    def _get_games(cls, year):
        url = '{}/worldcup/archive/{}/matches/index.html'.format(
            cls.BASE_URL, year)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        games = soup.select('div.matches div.mu.result a.mu-m-link')
        ids = []
        for a in games:
            href = a['href'].strip()
            result = re.search(
                '/worldcup/matches/round=(.*)/match=(.*)/index.html', href)
            ids.append((result.group(1), result.group(2)))
        return ids

    @classmethod
    def _get_results(cls, game):
        url = '{}/worldcup/matches/round={}/match={}/index.html'.format(
            cls.BASE_URL, game[0], game[1])
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        title = soup.select_one('h1.title').get_text().strip()
        title_re = re.search('([0-9]{4}) FIFA World Cup (.*?) ?™', title)
        scores = soup.select_one('div.s span.s-scoreText').get_text().split('-')
        home_scorers = soup.select('div.t-scorer.home li.mh-scorer')
        away_scorers = soup.select('div.t-scorer.away li.mh-scorer')

        def get_goals(scorers):
            goals = []
            for scorer in scorers:
                player = scorer.find('span', class_='p-n-webname').get_text()
                minutes_div = scorer.find('span', class_='ml-scorer-evmin')
                minutes = minutes_div.find_all('span')
                for span in minutes:
                    text = span.get_text()
                    clean = text
                    for c in [',', '\'', 'PEN', 'OG']:
                        clean = clean.replace(c, '').strip()
                    goals.append({
                        'player': player,
                        'minute': '{}\''.format(clean),
                        'penalty': 'PEN' in text,
                        'own_goal': 'OG' in text,
                    })
            return goals

        return {
            'league': cls.LEAGUE_NAME,
            'year': title_re.group(1),
            'host': title_re.group(2),
            'stadium': soup.select_one('span.mh-i-stadium').get_text().strip(),
            'date': soup.select_one('div.mh-i-datetime').get_text().strip(),
            'round': soup.select_one('div.mh-i-round').get_text().strip(),
            'home_team': soup.select_one('div.t.home .t-nText').get_text().strip(),
            'home_score': int(scores[0]),
            'home_goals': get_goals(home_scorers),
            'away_team': soup.select_one('div.t.away .t-nText').get_text().strip(),
            'away_score': int(scores[1]),
            'away_goals': get_goals(away_scorers),
        }

    @classmethod
    def run(cls):
        logging.info('Running FIFA scrape...')

        years = cls._get_years()
        logging.info('Found {} years to pull data from.'.format(len(years)))

        games = []
        for year in years:
            year_games = cls._get_games(year)
            logging.info('Found {} games in {}.'.format(len(year_games), year))
            games.extend(year_games)
        logging.info('Found {} total games.'.format(len(games)))

        results = []
        logging.info('Beginning results scrape. This may take some time...')
        for i, game in enumerate(games):
            results.append(cls._get_results(game))
            if i % 10 == 0:
                cls.save(results)
                logging.info('Finished game {} of {}.'.format(i, len(games)))
        logging.info('Found {} total results.'.format(len(results)))

        cls.save(results)
