import logging

import requests
from openi.settings import *
from openi.utils import file_utils

"""
APIS
"""
class OpeniAPI:

    def __init__(self, endpoint: str = None, token: str = None):
        self.endpoint = file_utils.get_token()["endpoint"] + API.VERSION if endpoint is None else endpoint + API.VERSION
        self.token = file_utils.get_token()["token"] if token is None else token

    def catch_auth_error(self, x):
        if x.status_code == 401:
            msg = f"❌ {x} {x.reason} - failed to connecting OPENI, please check your `token` or permssion."
            logging.error(msg)
            raise PermissionError(msg)
        if x.status_code == 404:
            msg = f"❌ {x} {x.reason} - failed to connecting OPENI, either incorrect `owner/repo` or `endpoint`."
            logging.error(msg)
            raise ConnectionError(msg)
        if x.raise_for_status():
            logging.error(x.raise_for_status())
            x.raise_for_status()

    def login_check(self) -> str:
        params = {
            "access_token": self.token
        }
        x = requests.get(f'{self.endpoint}/user', params=params)
        logging.info(f"GET {x.url}")
        self.catch_auth_error(x)
        logging.info(f"{x} {x.url} {x.json()}")
        return x.json()["username"]

    def get_dataset(self, repo_id):
        params = {
            "access_token": self.token
        }
        x = requests.get(f'{self.endpoint}/datasets/{repo_id}', params=params)
        logging.info(f"GET {x.url}")
        self.catch_auth_error(x)
        logging.info(f"{x} {x.url} {x.json()}")
        return x.json()["data"]

    def get_dataset_attachment(self, repo_id: str, upload_type: str):
        params = {
            "access_token": self.token,
            "type": upload_type
        }
        x = requests.get(f'{self.endpoint}/datasets/{repo_id}/current_repo', params=params)
        logging.info(f"GET {x.url}")
        self.catch_auth_error(x)
        logging.info(f"{x} {x.url} {x.json()}")
        return x.json()

    def get_chunks(self, _file):
        params = {
            "access_token": self.token,
            "dataset_id": _file["dataset_id"],
            "md5": _file["md5"],
            "file_name": _file["filename"],
            "type": _file["upload_type"],
        }
        x = requests.get(f'{self.endpoint}/attachments/get_chunks', params=params)
        logging.info(f"GET {x.url}")
        if x.ok:
            logging.info(f"{x} {x.url} {x.json()}")
            return x.json()
        else:
            msg = f'❌ {x} {x.reason} {x.text}'
            logging.error(msg)
            raise ConnectionRefusedError(msg)

    def get_multipart_url(self, chunk_number: int, chunk_size: int, _file: dict):
        params = {
            "access_token": self.token,
            "dataset_id": _file["dataset_id"],
            "file_name": _file["filename"],
            "type": _file["upload_type"],
            "chunkNumber": chunk_number,
            "size": chunk_size,
            "uploadID": _file["upload_id"],
            "uuid": _file["uuid"]
        }
        x = requests.get(f'{self.endpoint}/attachments/get_multipart_url', params=params)
        logging.info(f"GET {x.url}")
        if x.ok:
            logging.info(f"{x} {x.url} {x.json()}")
            return x.json()["url"]
        else:
            msg = f'❌ {x} {x.reason}'
            logging.error(msg)
            raise ConnectionRefusedError(msg)

    def put_upload(self, url, data, upload_type):
        headers = {"Content-Type": "text/plain"} if upload_type == 0 else {}
        x = requests.put(url, data=data, headers=headers)
        logging.info(f"PUT {x.url}")
        try:
            logging.info(f"{x} {x.url} {x.headers}")
            return x.headers["ETag"]
        except:
            msg = f'❌ {x} {x.reason} {x.text}'
            logging.error(msg)
            raise ConnectionRefusedError(msg)

    def new_multipart(self, _file):
        params = {
            "access_token": self.token,
            "dataset_id": _file["dataset_id"],
            "md5": _file["md5"],
            "file_name": _file["filename"],
            "type": _file["upload_type"],
            "totalChunkCounts": _file["total_chunks_count"],
            "size": _file["size"]
        }
        x = requests.get(f'{self.endpoint}/attachments/new_multipart', params=params)
        logging.info(f"GET {x.url}")
        if x.ok:
            if x.json()["result_code"] == "0":
                logging.info(f"{x} {x.url} {x.json()}")
                return x.json()["uuid"], x.json()["uploadID"]
            else:
                logging.error(f'❌ {x} {x.reason} {x.json()}')
                raise ConnectionRefusedError(
                    f'❌ {x} {x.reason} {x.json()["msg"]}')
        else:
            msg = f'❌ {x} {x.reason}'
            logging.error(msg)
            raise ConnectionRefusedError(msg)

    def complete_multipart(self, _file):
        params = {
            "access_token": self.token,
            "dataset_id": _file["dataset_id"],
            "file_name": _file["filename"],
            "type": _file["upload_type"],
            "size": _file["size"],
            "uploadID": _file["upload_id"],
            "uuid": _file["uuid"]
        }
        x = requests.post(f'{self.endpoint}/attachments/complete_multipart', params=params)
        logging.info(f"POST {x.url}")
        if x.ok:
            if x.json()["result_code"] == "-1":
                logging.error(f'❌ {x} {x.reason} {x.json()}')
                raise ConnectionRefusedError(
                    f'❌ {x} {x.reason} {x.json()["msg"]}')
            else:
                logging.info(f"{x} {x.url} {x.json()}")
        else:
            msg = f'❌ {x} {x.reason} {x.text}'
            logging.error(msg)
            raise ConnectionRefusedError(msg)
    def download_attachments(self, uuid: str, upload_type: int):
        params = {
            "access_token": self.token,
            "type": upload_type
        }
        x = requests.get(f"{self.endpoint}/attachments/{uuid}", params=params,
                                allow_redirects=True, stream=True)
        logging.info(f"GET {x.url}")
        self.catch_auth_error(x)
        logging.info(f"{x} {x.url}")
        return x