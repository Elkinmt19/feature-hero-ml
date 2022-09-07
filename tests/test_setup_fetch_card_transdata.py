# Built-in imports
import os
import unittest

# External imports
import pandas as pd

# Own imports
from setup_scripts import get_path_dir as gpd
from setup_scripts import fetch_card_transdata as fct

_ = fct.pipeline()

TRANSFORMED_FILE = os.path.join(
    gpd.get_desired_folder_path("feature_hero_repo"),
    "offline_store",
    "card_transdata.parquet",
)


class TestSetupFetchCardTransdata(unittest.TestCase):
    def test_fraud_proportion(self):
        df = pd.read_parquet(TRANSFORMED_FILE)

        self.assertEqual(df["fraud"].value_counts()[0], 912597)
        self.assertEqual(df["fraud"].value_counts()[1], 87403)

    def test_day_proportion(self):
        df = pd.read_parquet(TRANSFORMED_FILE)
        df["day"] = df["event_timestamp"].apply(lambda x: x.day)

        self.assertEqual(df["day"].value_counts()[19], 699999)
        self.assertEqual(df["day"].value_counts()[20], 300001)

    def test_transaction_uuid_unique_proportion(self):
        df = pd.read_parquet(TRANSFORMED_FILE)

        self.assertEqual(df["transaction_uuid"].unique().shape[0], df.shape[0])

    def test_user_id_unique_proportion(self):
        df = pd.read_parquet(TRANSFORMED_FILE)

        self.assertEqual(df["user_id"].unique().shape[0], 1)
