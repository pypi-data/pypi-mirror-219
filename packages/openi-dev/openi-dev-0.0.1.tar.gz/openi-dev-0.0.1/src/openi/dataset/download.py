from openi.apis import OpeniAPI
from .dataset_file import *
from openi.utils import file_utils, logger
from openi.settings import *
from pathlib import Path
from tqdm import tqdm
import requests
import os
import logging
logger.setup_logger()

def download_with_tqdm(
        response: requests.Response,
        filepath: str
):
    file_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB

    if os.path.exists(filepath):
        filepath = file_utils.rename_existing_file(filepath)

    with tqdm(total=file_size, leave=True,
              unit='B', unit_scale=True, unit_divisor=1000,
              bar_format='{desc}{percentage:3.0f}%|{bar}{r_bar}',
              desc=f'{logger.get_time()} - Downloading: ',
              dynamic_ncols=True) as pbar:

        with open(filepath, 'wb') as f:
            for data in response.iter_content(block_size):
                pbar.update(len(data))
                f.write(data)
    relapath = Path(filepath).relative_to(Path.cwd())
    print(f"{logger.get_time()} - 🎉 Download complete! file was saved to `{relapath}`")
    

def download_file(
        file: str,
        repo_id: str,
        cluster: str = "NPU",
        save_path: str = PATH.SAVE_PATH,
        #link_only: bool = False,
        endpoint: str = None,
        token: str = None
):
    _, repo = get_owner_repo(repo_id)
    upload_type, cluster = get_upload_type(cluster.upper())

    print(f'{logger.get_time()} - `{file}`({cluster}) searching file...')
    filepath = os.path.join(save_path, file)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    api = OpeniAPI(endpoint=endpoint, token=token)

    _datasets = api.get_dataset_attachment(repo_id=repo_id, upload_type=upload_type)
    if _datasets["data"] is not None:
        _dataset_info = next((d for d in _datasets["data"] if d["repo"]["name"] == repo), None)
    if _datasets["count"] == 0 or _dataset_info is None:
        raise ValueError(
            f"❌ `{repo_id}`: dataset not created OR no zipfile({cluster.upper()}) found.")

    if _dataset_info["attachments"] is not None:
        _attachment = next((d for d in _dataset_info["attachments"] if d["name"] == file), None)
    if _attachment is None:
        raise ValueError(
            f"❌ `{file}`({cluster.upper()}): file not found in `{repo_id}`")

    uuid = _attachment["uuid"]

    response = api.download_attachments(uuid, upload_type)
    download_with_tqdm(response, filepath)

def download_file_link(
        link: str,
        save_path: str = PATH.SAVE_PATH,
        link_only: bool = False,
        endpoint: str = None,
        token: str = None
):

    api = OpeniAPI(endpoint=endpoint, token=token)

    _attach = link.split('attachments/')[-1]
    uuid = _attach.split('?')[0]
    upload_type = int(_attach.split('=')[-1])
    cluster = "NPU" if upload_type == 1 else "GPU"

    response = api.download_attachments(uuid, upload_type)
    filename = response.url.split('%22')[-2]

    print(f'{logger.get_time()} - `{filename}`({cluster}) searching file...')

    if link_only:
        print(f'{logger.get_time()} - 🎉 Download link: {response.url}')
    else:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        filepath = os.path.join(save_path, filename)
        download_with_tqdm(response, filepath)

        