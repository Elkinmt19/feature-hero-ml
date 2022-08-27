# Built-in imports 
import os
import logging
from typing import Union

# External imports
import pandas as pd
from dotenv import (
    load_dotenv, find_dotenv
)

# Own imports
from setup_scripts import get_path_dir as gpd

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d-%(levelname)s-%(message)s'
)

def _get_train_val_dataset() -> Union[pd.DataFrame,pd.DataFrame]:
    logging.info("Fetching the card_transdata.parquet file")
    dataset = pd.read_parquet(os.path.join(
        gpd.get_desired_folder_path("feature_hero_repo"),
        "offline_store",
        "card_transdata.parquet"
    ))

    dataset["day"] = dataset["event_timestamp"].apply(lambda x: x.day)

    logging.info("Splitting the dataset into traning and validation datasets")
    train_dataset = dataset.query("day == 19").iloc[:,:-1].reset_index(drop=True)
    val_dataset = dataset.query("day == 20").iloc[:,:-1].reset_index(drop=True)

    return train_dataset, val_dataset

def _load_train_val_dataset(train_ds:pd.DataFrame, val_ds:pd.DataFrame) -> int:
    logging.info("Loading the training dataset")
    train_ds.to_parquet(os.path.join(
        gpd.get_desired_folder_path("feature_hero_repo"),
        "offline_store",
        "training_card_transdata.parquet"
    ))

    logging.info("Loading the validation dataset")
    val_ds.to_parquet(os.path.join(
        gpd.get_desired_folder_path("feature_hero_repo"),
        "offline_store",
        "validation_card_transdata.parquet"
    ))

def pipeline():
    logging.info("Starting data pipeline")

    logging.info("<_get_train_val_dataset> task started")
    train_ds, val_ds = _get_train_val_dataset()

    logging.info("<_load_train_val_dataset> task started")
    _load_train_val_dataset(train_ds, val_ds)

    logging.info("Data pipeline finished")

if __name__=="__main__":
    pipeline()