import os
from pathlib import Path

import requests


PINATA_BASE_URL = "https://api.pinata.cloud"
endpoint = "pinning/pileFileToIPFS"
file_path = "./img/pug.png"
filename = file_path.split("/")[-1]
headers = {
    "pinata_api_key": os.getenv("PINATA_API"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


def main():
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"files": (filename, image_binary)},
            headers=headers,
        )
