# NBA Metrics

An end-to-end ETL pipeline that pulls NBA shot data, cleans and models it into shooting zones, and visualizes it as hex-bin shot charts and efficiency breakdowns. Built to demonstrate a full pull, clean, model, visualize data-engineering loop.

## Overview

NBAMetrics hits the NBA's public stats endpoints through the `nba_api` package, caches the raw responses, transforms them into model-ready data (zone buckets, FG%, effective FG%), and produces both Python charts and a Power BI dashboard from the cleaned output.

The point of the project is the pipeline, not just the chart. Raw pulls are kept separate from processed data so the API only gets hit once, and the whole flow is orchestrated through a single entry point.

## Pipeline

```
extract  ->  transform  ->  load  ->  visualize
```

1. **Extract** pulls shot chart detail and play-by-play data via `nba_api` and caches the raw responses to `data/raw/`.
2. **Transform** converts raw court coordinates, buckets each shot into a zone (restricted area, paint, mid-range, corner three, above the break), and computes FG% and eFG% per zone.
3. **Load** writes the cleaned, model-ready CSVs to `data/processed/`, which serve as the source for Power BI.
4. **Visualize** draws the court and overlays a hex-bin shot chart, saving outputs to `outputs/charts/`.

## Project Structure

```
NBAMetrics/
├── config/settings.py        season, player/team IDs, output paths
├── data/raw/                 cached API pulls
├── data/processed/           cleaned, model-ready CSVs
├── src/extract.py            nba_api calls
├── src/transform.py          coordinate cleaning, zones, FG% calcs
├── src/load.py               write processed CSVs
├── src/visualize.py          matplotlib court + hexbin chart
├── notebooks/exploration.ipynb   scratch EDA
├── outputs/charts/           saved shot charts
└── main.py                   orchestrates the full pipeline
```

## Getting Started

```bash
git clone https://github.com/Sarim78/NBAMetrics.git
cd NBAMetrics
pip install -r requirements.txt
python main.py
```

Set the target season and player or team in `config/settings.py` before running.

## Tech Stack

Python, nba_api, pandas, matplotlib, and Power BI for the optional dashboard layer.

## Roadmap

Planned additions include team-level shot zone comparisons, season-over-season efficiency trends, and a small CLI to swap players without editing the config.

## License

MIT
