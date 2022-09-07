# Built-in imports
import os
from datetime import timedelta

# External imports
from feast import Field, Entity, FileSource, FeatureView, FeatureService
# Own imports
from scripts import get_path_dir as gpd
from feast.types import Int64, String, Float32

user_card_transactions_stats = FileSource(
    name="user_card_transactions_stats_source",
    path=os.path.join(
        gpd.get_desired_folder_path("offline_store"),
        "card_transdata.parquet",
    ),
    timestamp_field="event_timestamp",
)

user = Entity(name="user", join_keys=["user_id"])

user_card_transactions_stats_view = FeatureView(
    name="user_card_transactions_stats",
    entities=[user],
    ttl=timedelta(milliseconds=0.5),
    schema=[
        Field(name="transaction_uuid", dtype=String),
        Field(name="distance_from_home", dtype=Float32),
        Field(name="distance_from_last_transaction", dtype=Float32),
        Field(name="ratio_to_median_purchase_price", dtype=Float32),
        Field(name="repeat_retailer", dtype=Int64),
        Field(name="used_chip", dtype=Int64),
        Field(name="used_pin_number", dtype=Int64),
        Field(name="online_order", dtype=Int64),
        Field(name="fraud", dtype=Int64),
    ],
    online=True,
    source=user_card_transactions_stats,
    tags={
        "Author": "Elkin-Javier-Guerra-Galeano",
        "Role": "ML-Engineer",
        "Project": "Card-Transactions-fraud-detection",
    },
)

user_card_transactions_stats_fs = FeatureService(
    name="user_card_transaction_activity",
    features=[user_card_transactions_stats_view],
)
