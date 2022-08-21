# Built-in imports
import os
from datetime import datetime, timedelta

# External imports
import pandas as pd
from feast import FeatureStore
from feast.infra.offline_stores.file import SavedDatasetFileStorage
from dotenv import (
    load_dotenv, find_dotenv
)

# Own imports
import get_path_dir as gpd

_ = load_dotenv(find_dotenv())

TRAIN_LENGTH = 699999
VAL_LENGTH = 300001

train_entity_df = pd.DataFrame.from_dict(
    {
        "user_id": [os.environ.get('USER_ID')]*TRAIN_LENGTH,
        "event_timestamp": pd.date_range(
            start="2022-08-19",
            periods=TRAIN_LENGTH,
            freq='ms'
        ).to_list(),
    }
)

val_entity_df = pd.DataFrame.from_dict(
    {
        "user_id": [os.environ.get('USER_ID')]*VAL_LENGTH,
        "event_timestamp": pd.date_range(
            start="2022-08-20",
            periods=VAL_LENGTH,
            freq='ms'
        ).to_list(),
    }
)

store = FeatureStore(
    repo_path=gpd.get_desired_folder_path(".")
)

training_df = store.get_historical_features(
    entity_df=train_entity_df,
    features=store.get_feature_service("user_card_transaction_activity")
)

validation_df = store.get_historical_features(
    entity_df=val_entity_df,
    features=store.get_feature_service("user_card_transaction_activity")
)

store.create_saved_dataset(
    from_=training_df,
    name='training_dataset',
    storage=SavedDatasetFileStorage(
        path=os.path.join(
            gpd.get_desired_folder_path("offline_store"),
            "training_dataset.parquet"
        )
    )
)

store.create_saved_dataset(
    from_=validation_df,
    name='validation_dataset',
    storage=SavedDatasetFileStorage(
        path=os.path.join(
            gpd.get_desired_folder_path("offline_store"),
            "validation_dataset.parquet"
        )
    )
)