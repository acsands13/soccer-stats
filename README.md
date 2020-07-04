# Soccer Stats
If you had to bet, in which minute of a soccer game is a goal most likely to be
scored? This project contains the code used to scrape and analyze data from
the FIFA World Cup and the English Premier League to answer that question.

A write-up of this project can be found here:
[Cliffhanger Endings in Soccer](https://alexsands.com/cliffhanger-endings-in-soccer/).

The data used in the analysis can be found in
[`/data`](https://github.com/acsands13/soccer-stats/tree/master/data).

The plots used in the write-up can be found in
[`/plots`](https://github.com/acsands13/soccer-stats/tree/master/plots).


## Installation
Create a virtual environment and install this project's dependencies with:
```sh
pip3 install -r requirements.txt
```

## Run
To run the scraper to collect the data for analysis, run the following:
```sh
python3 -m soccer_stats --scrape fifa epl
```

To create the plots once the data has been scraped and is located in `/data`:
```sh
python3 -m soccer_stats --plot fifa epl
```

For help with the available command line options, run:
```sh
python3 -m soccer_stats --help
```
