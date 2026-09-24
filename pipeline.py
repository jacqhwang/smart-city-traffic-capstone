import logging
import sys
import pandas as pd

# Create a logger for this module
logger = logging.getLogger(__name__)


def setup_logging():
    """Configure logging to both the console and pipeline.log."""

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Log messages shown on screen
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Log messages saved to file
    file_handler = logging.FileHandler("pipeline.log")
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

def load_data(file_path):
    """Load the raw traffic CSV file."""

    try:
        df = pd.read_csv(file_path)

        logger.info(
            "Data loaded successfully: %d rows and %d columns",
            df.shape[0],
            df.shape[1]
        )

        return df

    except FileNotFoundError:
        logger.error(
            "CSV file not found: %s",
            file_path,
            exc_info=True
        )
        return None

    except pd.errors.ParserError:
        logger.error(
            "Error parsing CSV file: %s",
            file_path,
            exc_info=True
        )
        return None

def validate_schema(df):
    """Check that all expected columns are present."""

    expected_columns = [
        "holiday",
        "temp",
        "rain_1h",
        "snow_1h",
        "clouds_all",
        "weather_main",
        "weather_description",
        "date_time",
        "traffic_volume"
    ]

    missing_columns = [
        column for column in expected_columns
        if column not in df.columns
    ]

    if missing_columns:
        logger.error(
            "Schema validation failed. Missing columns: %s",
            missing_columns
        )
        return False

    logger.info("Schema validation successful.")
    return True 

def clean_data(df):
    """Clean the traffic dataset and log each cleaning operation."""

    df = df.copy()

    # Remove exact duplicate rows
    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()
    logger.info("Removed %d exact duplicate rows.", duplicate_count)

    # Convert date_time to datetime
    df["date_time"] = pd.to_datetime(
        df["date_time"],
        dayfirst=True,
        errors="coerce"
    )

    invalid_dates = df["date_time"].isna().sum()

    if invalid_dates > 0:
        logger.warning(
            "Found %d invalid date_time values.",
            invalid_dates
        )
        df = df.dropna(subset=["date_time"])

    logger.info("date_time converted to datetime format.")

    # Check for impossible temperature values
    invalid_temp = (df["temp"] <= 0).sum()

    if invalid_temp > 0:
        logger.warning(
            "Found %d invalid temperature values.",
            invalid_temp
        )

        df.loc[df["temp"] <= 0, "temp"] = pd.NA
    # Impute missing temperature values with the median
    missing_temp = df["temp"].isna().sum()

    if missing_temp > 0:
        median_temp = df["temp"].median()

        df["temp"] = df["temp"].fillna(median_temp)

        logger.info(
            "Imputed %d missing temperature values with median %.2f K.",
            missing_temp,
            median_temp
    )

    logger.info("Basic data cleaning completed.")

    logger.info(
        "Data cleaning finished. Final dataset contains %d rows.",
        len(df)
    )
    return df


if __name__ == "__main__":
    setup_logging()

    logger.info("Starting traffic data pipeline.")

    df = load_data("Metro_Interstate_Traffic_Volume.csv")

    if df is not None:
        if validate_schema(df):
            df_clean = clean_data(df)
            logger.info("Traffic data pipeline completed successfully.")
        else:
            logger.error("Pipeline stopped because schema validation failed.")
    else:
        logger.error("Pipeline stopped because data could not be loaded.")
    