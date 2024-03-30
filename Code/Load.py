from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import os
from prefect_gcp import GcpCredentials
from pathlib import PurePosixPath


@task()
def write_gcs(path: Path) -> None:
    # Upload local parquet file to GCS
    gcp_credentials = GcpCredentials.load("gcp-credentials")
    gcs_block = GcsBucket.load("gcs-bucket-spotify")

    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def load() -> None:
    """The main ETL function"""

    folder = f'API_DATA'

    for filename in os.listdir(folder):
        # folder_path = os.path.join(folder, filename)
        # for filename in os.listdir(folder_path):
        file_path = os.path.join(folder, filename)
        write_gcs(file_path)


if __name__ == "__main__":
    load()
