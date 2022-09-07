import os
import uuid
import logging
from datetime import datetime, timedelta

import pandas as pd
from dotenv import find_dotenv, load_dotenv

from setup_scripts import get_path_dir as gpd

logging.basicConfig(level=logging.INFO, format='%(process)d-%(levelname)s-%(message)s')

_ = load_dotenv(find_dotenv())


def _transform_train_val(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Transforming the data base on the attribute <fraud>")

    # Non fraud observations
    non_fraud = df.query("fraud == 0.0")
    non_fraud_train = non_fraud.iloc[: int(non_fraud.shape[0] * 0.7), :]
    non_fraud_val = non_fraud.iloc[int(non_fraud.shape[0] * 0.7) :, :]

    # Fraud observations
    do_fraud = df.query("fraud == 1.0")
    do_fraud_train = do_fraud.iloc[: int(do_fraud.shape[0] * 0.7), :]
    do_fraud_val = do_fraud.iloc[int(do_fraud.shape[0] * 0.7) :, :]

    train = pd.concat([non_fraud_train, do_fraud_train]).reset_index(drop=True)
    val = pd.concat([non_fraud_val, do_fraud_val]).reset_index(drop=True)

    # Add the <event_timestamp> field based on the dataset
    logging.info("Adding the event_timestamp field")

    # Train dataset
    train["event_timestamp"] = train.index.to_series().apply(
        lambda x: datetime(2022, 8, 19) + timedelta(milliseconds=x)
    )

    timestamp_column = train.pop("event_timestamp")
    train.insert(0, 'event_timestamp', timestamp_column)

    # Validation dataset
    val["event_timestamp"] = val.index.to_series().apply(
        lambda x: datetime(2022, 8, 19) + timedelta(milliseconds=x) + timedelta(days=1)
    )

    timestamp_column = val.pop("event_timestamp")
    val.insert(0, 'event_timestamp', timestamp_column)

    df_transformed = pd.concat([train, val]).reset_index(drop=True)
    df_transformed["event_timestamp"] = pd.to_datetime(
        df_transformed["event_timestamp"], utc=True
    )

    return df_transformed


def _add_additional_attributes(df: pd.DataFrame) -> pd.DataFrame:
    # User id field
    logging.info("Adding the user_id")
    USER_ID = os.environ.get('USER_ID')
    df["user_id"] = USER_ID

    user_column = df.pop("user_id")
    df.insert(0, 'user_id', user_column)

    # Transaction_uuid field
    logging.info("Adding the transaction_uuid")
    df["transaction_uuid"] = df["distance_from_home"].apply(
        lambda x: str(uuid.uuid5(uuid.NAMESPACE_DNS, str(x)))
    )

    transaction_column = df.pop("transaction_uuid")
    df.insert(0, 'transaction_uuid', transaction_column)

    return df


def _fetch_data() -> pd.DataFrame:
    logging.info("The process of fetching the data source file is starting")
    card_transdf = pd.read_csv(
        os.path.join(gpd.get_desired_folder_path("data"), "card_transdata.csv")
    )

    logging.info("The fetching task is completed")
    return card_transdf


def _transform(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("The process of transformation of the data has begun")

    df_transformed = _add_additional_attributes(df)

    df_transformed = _transform_train_val(df_transformed)

    return df_transformed


def _load(df: pd.DataFrame) -> int:
    logging.info("Loading the resulted dataset into the right directory")
    df.to_parquet(
        os.path.join(
            gpd.get_desired_folder_path("feature_hero_repo"),
            "offline_store",
            "card_transdata.parquet",
        ),
        engine='pyarrow',
        compression=None,
        index=False,
    )
    logging.info("The loading task is completed")

    return 0


def pipeline():
    card_transdf = _fetch_data()

    card_transdf = _transform(card_transdf)

    _ = _load(card_transdf)


if __name__ == "__main__":
    pipeline()
