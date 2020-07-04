import logging
import argparse

from pathlib import Path

from soccer_stats.config import Config
from soccer_stats import stats
from soccer_stats import plotting as plot
from soccer_stats.scraping.fifa import FIFA
from soccer_stats.scraping.epl import EPL


def get_league_class(league):
    if league == 'fifa':
        return FIFA
    elif league == 'epl':
        return EPL
    else:
        return


def scrape_league(league):
    league_cls = get_league_class(league)
    league_cls.run()


def plot_league(league):
    league_cls = get_league_class(league)
    games = league_cls.load()

    Path('{}{}'.format(
        Config.PLOT_PATH, league_cls.OUTPUT_FILENAME)).mkdir(
        parents=True, exist_ok=True)

    plot.goals_per_minute(
        stats.all_goals_per_minute(games),
        '{}/all_goals_per_minute'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Number of Goals in Each Minute of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.all_goals_per_minute(games, buckets=2),
        '{}/all_goals_per_half'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Number of Goals in Each Half of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.all_goals_per_minute(games, buckets=4),
        '{}/all_goals_per_quarter'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Number of Goals in Each Quarter of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.all_goals_per_minute(games, buckets=10),
        '{}/all_goals_per_9_min'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Number of Goals in Every 9 Minutes of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.all_goals_per_minute(games, buckets=18),
        '{}/all_goals_per_5_min'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Number of Goals in Every 5 Minutes of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.game_winning_goals_per_minute(games),
        '{}/game_winner_goals_per_minute'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Game Winning Goals in Each Minute of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.game_winning_goals_per_minute(games, buckets=2),
        '{}/game_winner_goals_per_half'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Game Winning Goals in Each Half of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.game_winning_goals_per_minute(games, buckets=3),
        '{}/game_winner_goals_per_third'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Game Winning Goals in Each Third of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.game_winning_goals_per_minute(games, buckets=4),
        '{}/game_winner_goals_per_quarter'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Game Winning Goals in Each Quarter of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.game_winning_goals_per_minute(games, buckets=10),
        '{}/game_winner_goals_per_9_min'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Game Winning Goals in Every 9 Minutes of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_minute(
        stats.pk_goals_per_minute(games),
        '{}/pk_goals_per_minute'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Penalty Kick Goals in Each Minute of Game'.format(
            league_cls.LEAGUE_NAME),
    )

    plot.goals_per_year(
        stats.all_goals_per_game_per_year(games),
        '{}/all_goals_per_game_per_year'.format(league_cls.OUTPUT_FILENAME),
        title='{} - Goals Per Game in Each Year'.format(
            league_cls.LEAGUE_NAME),
    )


def run():
    # Configure the logging
    logging.basicConfig(
        format='%(levelname)s - %(asctime)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO)

    # Configure the ArgumentParser to get args passed to the program
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--plot',
        choices=['fifa', 'epl'], type=str, nargs='+',
        default=['fifa', 'epl'],
        help='run the analysis on each league and plot results',
    )
    parser.add_argument(
        '-s', '--scrape',
        choices=['fifa', 'epl'], type=str, nargs='+',
        help='run the scraper for specified league',
    )
    args = parser.parse_args()

    # Run the scrapers
    if args.scrape:
        for league in args.scrape:
            scrape_league(league)

    # Run the plotters
    if args.plot:
        for league in args.plot:
            plot_league(league)
