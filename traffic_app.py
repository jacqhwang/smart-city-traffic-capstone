import logging
import pandas as pd

from pipeline import setup_logging, load_data, validate_schema, clean_data
from feature_engineering import engineer_features

logger = logging.getLogger(__name__)

def query_by_hour(df, hour):
    """Return average traffic volume for a specified hour."""

    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23.")

    logger.info("CLI query: average traffic for hour %d.", hour)

    result = df.loc[
        df["hour"] == hour,
        "traffic_volume"
    ].mean()

    return result


def query_by_day(df, day):
    """Return average traffic volume for a specified day."""

    valid_days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    day = day.capitalize()

    if day not in valid_days:
        raise ValueError("Please enter a valid day of the week.")

    logger.info("CLI query: average traffic for %s.", day)

    result = df.loc[
        df["day_of_week"] == day,
        "traffic_volume"
    ].mean()

    return result


def query_by_weather(df, weather):
    """Return average traffic volume for a specified weather condition."""

    weather = weather.strip().title()

    available_weather = df["weather_main"].dropna().unique()

    if weather not in available_weather:
        raise ValueError("Weather condition not found in the dataset.")

    logger.info("CLI query: average traffic for weather condition %s.", weather)

    result = df.loc[
        df["weather_main"] == weather,
        "traffic_volume"
    ].mean()

    return result

def run_app(df):
    """Run the command-line traffic query application."""

    print("\nMetro Interstate Traffic Query App")
    print("1. Average traffic by hour")
    print("2. Average traffic by day of week")
    print("3. Average traffic by weather condition")

    choice = input("Choose an option (1, 2, or 3): ").strip()

    logger.info("CLI command selected: %s", choice)

    try:
        if choice == "1":
            hour = int(input("Enter hour (0-23): "))
            result = query_by_hour(df, hour)
            print(f"Average traffic volume at hour {hour}: {result:.0f}")

        elif choice == "2":
            day = input("Enter day of week: ")
            result = query_by_day(df, day)
            print(f"Average traffic volume on {day.capitalize()}: {result:.0f}")

        elif choice == "3":
            weather = input("Enter weather condition: ")
            result = query_by_weather(df, weather)
            print(f"Average traffic volume during {weather.title()}: {result:.0f}")

        else:
            logger.warning("Invalid CLI menu choice: %s", choice)
            print("Invalid choice. Please choose 1, 2, or 3.")

    except ValueError as error:
        logger.warning("Invalid user input: %s", error)
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    setup_logging()

    logger.info("Starting Traffic Query App.")

    df = load_data("Metro_Interstate_Traffic_Volume.csv")

    if df is not None and validate_schema(df):
        df = clean_data(df)
        df = engineer_features(df)
        run_app(df)
    else:
        logger.error("Traffic Query App could not start.")