import logging
import os
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def create_visualizations(df):
    """Create and save traffic visualisations."""

    # Create figures folder if it does not exist
    os.makedirs("figures", exist_ok=True)

    logger.info("Starting visualisation generation.")
    # Figure 1: Average traffic volume by hour
    hourly_traffic = df.groupby("hour")["traffic_volume"].mean()

    plt.figure(figsize=(10, 5))
    plt.plot(
        hourly_traffic.index,
        hourly_traffic.values,
        marker="o"
    )

    plt.title("Average Traffic Volume by Hour of Day")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Traffic Volume")
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.tight_layout()

    figure_path = "figures/traffic_by_hour.png"
    plt.savefig(figure_path)
    plt.close()

    logger.info("Saved visualisation: %s", figure_path)

     # Figure 2: Weekday vs weekend traffic by hour
    hourly_daytype = (
        df.groupby(["hour", "is_weekend"])["traffic_volume"]
        .mean()
        .unstack()
    )

    hourly_daytype.columns = ["Weekday", "Weekend"]

    plt.figure(figsize=(10, 5))

    plt.plot(
        hourly_daytype.index,
        hourly_daytype["Weekday"],
        marker="o",
        label="Weekday"
    )

    plt.plot(
        hourly_daytype.index,
        hourly_daytype["Weekend"],
        marker="o",
        label="Weekend"
    )

    plt.title("Average Traffic Volume by Hour: Weekday vs Weekend")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Traffic Volume")
    plt.xticks(range(0, 24))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    figure_path = "figures/weekday_vs_weekend_by_hour.png"
    plt.savefig(figure_path)
    plt.close()

    logger.info("Saved visualisation: %s", figure_path)

     # Figure 3: Average traffic volume by day of week
    day_order = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    daily_traffic = (
        df.groupby("day_of_week")["traffic_volume"]
        .mean()
        .reindex(day_order)
    )

    plt.figure(figsize=(9, 5))

    plt.plot(
        daily_traffic.index,
        daily_traffic.values,
        marker="o"
    )

    plt.title("Average Traffic Volume by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Traffic Volume")
    plt.grid(True)
    plt.tight_layout()

    figure_path = "figures/traffic_by_day_of_week.png"
    plt.savefig(figure_path)
    plt.close()

    logger.info("Saved visualisation: %s", figure_path)

    logger.info("Visualisation generation completed.")