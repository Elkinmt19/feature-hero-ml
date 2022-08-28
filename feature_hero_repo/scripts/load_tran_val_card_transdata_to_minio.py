# Built-in imports
import os
import logging

# External imports
from minio import Minio
from minio.error import S3Error

# Own imports
import get_path_dir as gpd

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d-%(levelname)s-%(message)s'
)

BUCKET_NAME = "card-transaction-data"
TRAIN_KEY = "training_card_transdata.parquet"
VAL_KEY = "validation_card_transdata.parquet"

def main():
    client = Minio(
        "minio:9000",
        access_key=os.environ.get('MINIO_ROOT_USER'),
        secret_key=os.environ.get('MINIO_ROOT_PASSWORD'),
        secure=False
    )

    logging.info("Creating the bucket if not exists")
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    else:
        logging.warn(f"Bucket '{BUCKET_NAME}' already exists")

    logging.info(f"Loading the <{TRAIN_KEY}>")
    client.fput_object(
        BUCKET_NAME,
        f"{TRAIN_KEY}",
        os.path.join(
            gpd.get_desired_folder_path("offline_store"),
            f"{TRAIN_KEY}"
        )
    )
    logging.info(
        f"'{TRAIN_KEY}' is successfully uploaded as "
        f"object '{TRAIN_KEY}' to bucket '{BUCKET_NAME}'."
    )

    logging.info(f"Loading the <{VAL_KEY}>")
    client.fput_object(
        BUCKET_NAME,
        f"{VAL_KEY}",
        os.path.join(
            gpd.get_desired_folder_path("offline_store"),
            f"{VAL_KEY}"
        )
    )
    logging.info(
        f"'{VAL_KEY}' is successfully uploaded as "
        f"object '{VAL_KEY}' to bucket '{BUCKET_NAME}'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)