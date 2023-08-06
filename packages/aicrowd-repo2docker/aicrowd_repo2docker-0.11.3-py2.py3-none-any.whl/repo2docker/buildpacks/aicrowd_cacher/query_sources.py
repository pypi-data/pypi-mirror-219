import csv
import logging
import os
from abc import ABC

import requests


class BaseQuerySource(ABC):
    def __init__(self, ro: bool = False):
        self.ro = ro
        self.log = logging.getLogger("repo2docker")

    def query(self, rhash: str, dhash: str) -> dict:
        return {}

    def update(self, rhash: str, dhash: str, tag: str):
        if self.ro:
            return

        # update the source about this new hashes


class APIQuerySource(BaseQuerySource):
    def __init__(self, ro: bool = False):
        super().__init__(ro)

        self.builder_api_endpoint = os.getenv(
            "AICROWD_R2D_IMAGE_BUILDER_ENDPOINT",
            "https://image-builder.aicrowd.com/api/v1",
        )
        self.api_key = os.getenv("SECRET_API_KEY")

    def query(self, rhash: str, dhash: str) -> dict:
        try:
            r = requests.get(
                f"{self.builder_api_endpoint}/caching/hasher",
                params={"rhash": rhash, "dhash": dhash},
                headers={"Authorization": self.api_key},
            )

            if not r.ok:
                return {}

            return r.json()
        except Exception as e:
            self.log.warn("Error in querying builder api about cache\n%s", str(e))
            return {}

    def update(self, rhash: str, dhash: str, tag: str):
        if self.ro or len(tag) == 0:
            return

        try:
            requests.post(
                f"{self.builder_api_endpoint}/caching/hasher",
                json={"rhash": rhash, "dhash": dhash, "image_tag": tag},
                headers={"Authorization": self.api_key},
            )
        except Exception as e:
            self.log.warn("Error in updating builder api about new repo\n%s", str(e))


class CSVQuerySource(BaseQuerySource):
    def __init__(self, ro: bool = False, csv_path: str = "/tmp/aicrowd-r2d-cache.csv"):
        super().__init__(ro)

        self.csv_path = csv_path

    def query(self, rhash: str, dhash: str) -> dict:
        available_images = {"repo": [], "deps": []}
        try:
            with open(self.csv_path, "r") as f:
                reader = csv.reader(f)

                for row in reader:
                    if row[0] == rhash:
                        available_images["repo"].append(row[2])
                    if row[1] == dhash:
                        available_images["deps"].append(row[2])
        except Exception as e:
            self.log.warn("Error in reading the csv file\n%s", str(e))
            return {}

        return available_images

    def update(self, rhash: str, dhash: str, tag: str):
        if self.ro:
            return

        try:
            with open(self.csv_path, "a+") as f:
                writer = csv.writer(
                    f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONE
                )
                writer.writerow([rhash, dhash, tag])
        except Exception as e:
            self.log.warn("Error in updating the csv file\n%s", str(e))
            return {}
