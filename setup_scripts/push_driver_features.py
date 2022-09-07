import json
import requests
import pandas as pd
from datetime import datetime

event_dict = {
    "driver_id": [1001],
    "event_timestamp": [str(datetime(2021, 5, 13, 10, 59, 42))],
    "created": [str(datetime(2021, 5, 13, 10, 59, 42))],
    "conv_rate": [1.0],
    "acc_rate": [1.0],
    "avg_daily_trips": [1000],
    "string_feature": "test2",
}
push_data = {
    "push_source_name":"driver_stats_push_source",
    "df":event_dict,
    "to":"online",
}
response = requests.post(
    "http://localhost:6566/push",
    data=json.dumps(push_data),
)

print(f"Status Code: {response.status_code}")
print(response.text)
