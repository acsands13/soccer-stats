import logging
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from soccer_stats.scraping import Scraper


class EPL(Scraper):
    LEAGUE_NAME = 'English Premier League'
    BASE_URL = 'https://www.premierleague.com'
    OUTPUT_FILENAME = 'epl'

    @classmethod
    def _get_results(cls, i):
        url = '{}/match/{}'.format(cls.BASE_URL, i)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        # Do not parse if we've found a page that doesn't exist
        content = soup.find('div', class_='matchCentre')
        if content is None:
            logging.warning('Ended scraping on {} due to no content'.format(i))
            return

        # Do not parse if this isn't a Premier League game
        title = soup.find('title').get_text().strip()
        if not title.endswith('| Premier League'):
            return

        # Do not parse if this is a blank match
        utc_div = soup.select_one('div.matchDate')
        if utc_div is None:
            return

        utc = utc_div.get('data-kickoff', '').strip()
        date = datetime.fromtimestamp(int(utc) / 1000.0)
        scores = soup.select_one('div.score.fullTime').get_text().split('-')
        scores = [int(s) for s in scores]
        home_scorers = soup.select('div.matchEvents div.home div.event')
        away_scorers = soup.select('div.matchEvents div.away div.event')

        # Do not parse if we don't have the proper goal scoring data
        if sum(scores) > 0 and len(home_scorers + away_scorers) == 0:
            return

        def get_goals(scorers):
            goals = []
            for scorer in scorers:
                scorer.find('div', class_='icnContainer').decompose()
                player = scorer.find('a').get_text().strip()
                all_text = scorer.get_text().strip()
                minutes = all_text.replace(player, '').strip().split(',')
                for minute in minutes:
                    clean = minute
                    for c in [' ', '\'', '(pen)', '(og)']:
                        clean = clean.replace(c, '').strip()
                    goals.append({
                        'player': player,
                        'minute': '{}\''.format(clean),
                        'penalty': '(pen)' in minute,
                        'own_goal': '(og)' in minute,
                    })
            return goals

        return {
            'league': cls.LEAGUE_NAME,
            'year': date.year,
            'stadium': soup.select_one('div.stadium').get_text().strip(),
            'date': date.strftime('%Y-%m-%d %H:%M'),
            'round': soup.select_one('header.mcHeader div.dropDown div.current div.long').get_text().strip(),
            'home_team': soup.select_one('div.team.home a.teamName span.long').get_text().strip(),
            'home_score': scores[0],
            'home_goals': get_goals(home_scorers),
            'away_team': soup.select_one('div.team.away a.teamName span.long').get_text().strip(),
            'away_score': scores[1],
            'away_goals': get_goals(away_scorers),
        }

    @classmethod
    def run(cls):
        logging.info('Running EPL scrape...')

        results = []
        logging.info('Beginning results scrape. This may take some time...')
        i = 9232  # First game in the 2013/14 season
        while i <= 38683:  # Last game in the 2018/19 season
            if i % 10 == 0:
                cls.save(results)
                logging.info('Finished game {}.'.format(i))
            try:
                result = cls._get_results(i)
                if result is not None:
                    results.append(result)
                i += 1
            except IndexError:
                break

        logging.info('Found {} total results.'.format(len(results)))

        cls.save(results)
