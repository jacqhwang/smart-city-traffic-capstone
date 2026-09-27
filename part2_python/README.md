# Metro Interstate Traffic Volume Analysis

## Project Overview

This project analyses the Metro Interstate Traffic Volume dataset using a reproducible Python workflow. It builds on the exploratory analysis from Part 1 and focuses on data cleaning, feature engineering, visualisation, logging, automated testing, and a command-line query application.

## Project Structure

- `pipeline.py` - loads, validates and cleans the traffic dataset
- `feature_engineering.py` - creates features for analysis and modelling
- `visualizations.py` - generates and saves traffic visualisations
- `traffic_app.py` - command-line application for querying traffic patterns
- `test_pipeline.py` - automated tests for key pipeline functions
- `Capstone_Part2.ipynb` - exploratory analysis and development notebook
- `figures/` - saved visualisation outputs
- `pipeline.log` - pipeline execution log

## Data Preparation

The pipeline:
- validates the expected dataset schema
- removes exact duplicate rows
- converts `date_time` to datetime format
- identifies invalid temperature values
- imputes invalid temperature values using the median
- logs important processing events and warnings

## Feature Engineering

The project creates:
- hour of day
- day of week
- weekday/weekend indicator
- cyclical hour encoding using sine and cosine
- one-hot encoded weather categories
- scaled temperature and cloud-cover variables
- data-driven Low, Medium and High traffic categories using tertiles

## Visualisations

Three figures are generated and saved:

1. Average traffic volume by hour of day
2. Weekday versus weekend traffic volume by hour
3. Average traffic volume by day of week

## Command-Line Application

The traffic query application allows users to obtain average traffic volume by:

1. hour of day
2. day of week
3. weather condition

Invalid user inputs are handled and relevant events are logged.

## Automated Testing

`test_pipeline.py` tests:
- schema validation
- duplicate removal
- datetime conversion

The tests can be run with:

```bash
python -m pytest test_pipeline.py -v
```

## Requirements

The project requires Python and the following main packages:

- pandas
- numpy
- matplotlib
- pytest

## Running the Project

Run the main pipeline with:

```bash
python pipeline.py
```

Run the traffic query application with:

```bash
python traffic_app.py
```

Run the automated tests with:

```bash
python -m pytest test_pipeline.py -v
```

