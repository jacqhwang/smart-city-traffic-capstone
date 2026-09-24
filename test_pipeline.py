import pandas as pd

from pipeline import validate_schema, clean_data


def create_test_data():
    """Create a small sample dataset for testing."""

    return pd.DataFrame({
        "holiday": [None, None],
        "temp": [280.0, 285.0],
        "rain_1h": [0.0, 0.0],
        "snow_1h": [0.0, 0.0],
        "clouds_all": [40, 75],
        "weather_main": ["Clouds", "Clear"],
        "weather_description": ["scattered clouds", "sky is clear"],
        "date_time": [
            "2016-01-01 08:00:00",
            "2016-01-01 09:00:00"
        ],
        "traffic_volume": [4000, 5000]
    })

def test_validate_schema():
    """Test that the correct schema passes validation."""

    df = create_test_data()

    assert validate_schema(df) is True


def test_clean_data_removes_duplicates():
    """Test that duplicate rows are removed."""

    df = create_test_data()

    # Add an exact duplicate row
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    cleaned_df = clean_data(df)

    assert len(cleaned_df) == 2


def test_clean_data_converts_datetime():
    """Test that date_time is converted to datetime."""

    df = create_test_data()

    cleaned_df = clean_data(df)

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned_df["date_time"]
    )