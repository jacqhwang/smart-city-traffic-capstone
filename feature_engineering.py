import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def engineer_features(df):
    """Create features for traffic analysis and modelling."""

    df = df.copy()

    logger.info("Starting feature engineering.")

    # Time-based features
    df["hour"] = df["date_time"].dt.hour
    df["day_of_week"] = df["date_time"].dt.day_name()
    df["is_weekend"] = df["date_time"].dt.dayofweek.isin([5, 6]).astype(int)

    logger.info(
        "Created hour, day_of_week and is_weekend features."
    )
    # Cyclical encoding of hour
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    logger.info(
        "Created cyclical hour features: hour_sin and hour_cos."
    )

    # One-hot encode weather categories
    weather_encoded = pd.get_dummies(
        df["weather_main"],
        prefix="weather",
        dtype=int
    )

    df = pd.concat([df, weather_encoded], axis=1)

    logger.info(
        "One-hot encoded weather_main into %d weather features.",
        weather_encoded.shape[1]
    )

    # Standardise continuous variables
    for column in ["temp", "clouds_all"]:
        mean_value = df[column].mean()
        std_value = df[column].std()

        df[column + "_scaled"] = (
            (df[column] - mean_value) / std_value
        )

        logger.info(
            "Standardised continuous variable: %s.",
            column
        )

    # Create data-driven congestion categories using tertiles
    df["traffic_category"] = pd.qcut(
        df["traffic_volume"],
        q=3,
        labels=["Low", "Medium", "High"]
    )

    logger.info(
        "Created data-driven traffic congestion categories using tertiles."
    )
    
    return df