from openi.utils import file_utils,logger
from openi.settings import *
import os
import logging
logger.setup_logger()


"""
Dataset File class
"""
class DatasetFile:
    """
    File object in a dataset from https://openi.pcl.ac.cn/

    Attributes:
        filepath (`str`):
            filepath on local machine
        owner (`str`):
            username of target repo owner
        repository (`str`):
            repository name to which the dataset file is uploaded
        upload_type (`str`, [`0`,`1`], defaults to `1`):
            cloud storage type, `0` for GPU and `1` for NPU

        filename (`str`):
            filepath on local machine
        size (`str`):
            filepath on local machine
        upload_id (`str`):
            filepath on local machine
        uuid (`str`):
            filepath on local machine
        token (`str`):
            filepath on local machine
    """

    def __init__(self, file: str, repo_id: str, cluster: str, **kwargs):

        self.filepath = os.path.abspath(file)
        self.filename = os.path.basename(file)
        self.size = os.path.getsize(file)

        self.owner, self.repository = get_owner_repo(repo_id)
        self.upload_type, self.cluster = get_upload_type(cluster)

        self.chunk_size = DATASET.SMALL_FILE_CHUNK_SIZE if self.size < DATASET.SMALL_FILE_LIMIT \
            else DATASET.LARGE_FILE_CHUNK_SIZE
        self.total_chunks_count = file_utils.get_file_chunk(chunk_size=self.chunk_size, filesize=self.size)

        self.uuid = None
        self.md5 = None
        self.upload_id = None
        self.dataset_id = None

    def upload_size_check(self):
        if self.size == 0:
            msg = f"❌ `{self.filename}` file size is 0"
            logging.error(msg)
            raise ValueError(msg)
        if self.size > DATASET.MAX_FILE_SIZE:
            msg = f"❌ `{self.filename}` file size exceeds {DATASET.MAX_FILE_SIZE_GB}GB"
            logging.error(msg)
            raise ValueError(msg)

def get_owner_repo(repo_id: str):
    try:
        owner = repo_id.split("/")[0]
        repository = repo_id.split("/")[1]
        return owner, repository
    except:
        msg = f"❌ argument `repo_id` must be in the form of `owner/repo`"
        logging.error(msg)
        raise ValueError(msg)

def get_upload_type(cluster: str):
    try:
        upload_type = DATASET.SOTRAGE_TYPE[cluster]
        cluster = cluster
        return upload_type, cluster
    except:
        msg = f"❌ argument `cluster` must be either `GPU` or `NPU`"
        logging.error(msg)
        raise ValueError(msg)
        # print("❌ argument `cluster` must be either `GPU` or `NPU`")
        # raise SystemExit()

