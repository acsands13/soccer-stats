# Soccer Stats


## Data
The data the analysis was performed on can be found in
[`/data`](https://github.com/acsands13/soccer-stats/tree/master/data).


## Plots
The plots used in the summary article can be found in
[`/plots`](https://github.com/acsands13/soccer-stats/tree/master/plots).


## Running the Code

### Installation
To install the dependencies for a project, create a virtual environment
and install the requirements with:
```sh
pip3 install -r requirements.txt
```

### Run
To run the scraper to collect the data for analysis, run the following:
```sh
python3 -m soccer_stats -scrape [fifa, epl]
```

To create the plots once the data has been scraped and is located in `/data`:
```sh
python3 -m soccer_stats -plot [fifa, epl]
```

For help with the available command line options, run:
```sh
python3 -m soccer_stats --help
```
