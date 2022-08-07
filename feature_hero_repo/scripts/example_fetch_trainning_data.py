from datetime import datetime, timedelta
import pandas as pd

from feast import FeatureStore
from scripts import get_path_dir as gpd

# The entity dataframe is the dataframe we want to enrich with feature values
entity_df = pd.DataFrame.from_dict(
    {
        # entity's join key -> entity values
        "driver_id": [1001, 1002, 1003],

        # label name -> label values
        "label_driver_reported_satisfaction": [1, 5, 3],

        # "event_timestamp" (reserved key) -> timestamps
        "event_timestamp": [
            datetime.now() - timedelta(minutes=11),
            datetime.now() - timedelta(minutes=36),
            datetime.now() - timedelta(minutes=73),
        ],
    }
)

store = FeatureStore(
    repo_path=gpd.get_desired_folder_path(".")
)

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
).to_df()

print("----- Feature schema -----\n")
print(training_df.info())

print()
print("----- Example features -----\n")
print(training_df.head())