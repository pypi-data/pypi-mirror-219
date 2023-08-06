from .dataset_file import *
from openi.apis import OpeniAPI
from openi.utils import file_utils, logger
from openi.settings import *
from tqdm import tqdm
import logging
logger.setup_logger()

def upload_with_tqdm(
        _file: DatasetFile,
        api: OpeniAPI,
        upload_chunks: list
):  
    chunk_size = _file.chunk_size
    _progress = chunk_size * (_file.total_chunks_count - len(upload_chunks))
    #_desc = 'Uploading' if _progress == 0 else 'Continue uploading'

    with tqdm(total=_file.size, leave=True, initial=_progress,
              unit='B', unit_scale=True, unit_divisor=1000,
              bar_format='{desc}{percentage:3.0f}%|{bar}{r_bar}',
              desc=f'{logger.get_time()} - Uploading: ',
              dynamic_ncols=True) as pbar:

        msg = f'start uploading with progress bar, file object {_file.__dict__}'
        logging.info(msg)

        # upload_chunks
        for n in upload_chunks:
            start_position = (n - 1) * chunk_size
            real_chunk_size = min(chunk_size, _file.size - start_position)
            
            data = file_utils.read_file_chunk(_file.filepath, start_position, real_chunk_size)
            for i in range(real_chunk_size):
                pbar.update(1)

            url = api.get_multipart_url(n, chunk_size, _file.__dict__)
            etag = api.put_upload(url, data, _file.upload_type)
            if etag is None:
                msg = f'❌ Upload failed: {_file.filename}({_file.cluster}) '\
                    f'chunk {n} failed to upload.'
                logging.error(msg)
                raise RuntimeError(msg)



def upload_file(
        file: str,
        repo_id: str,
        cluster: str = "NPU",
        endpoint: str = None,
        token: str = None
):  

    api = OpeniAPI(endpoint=endpoint, token=token)

    _dataset_info = api.get_dataset(repo_id=repo_id)
    if _dataset_info == []:
        msg = f"❌ `{repo_id}` no dataset was found, please create a dataset first before upload files."
        logging.error(msg)
        raise ValueError(msg)
    
    # file object init
    _file = DatasetFile(file=file, repo_id=repo_id, cluster=cluster.upper())
    _file.upload_size_check()
    _file.dataset_id = _dataset_info[0]["id"]

    msg = f'{logger.get_time()} - `{_file.filename}`({_file.cluster}) calculating md5...'
    logging.info(msg)
    print(msg)
    try:
        _file.md5 = file_utils.calculateMD5(_file.filepath)
    except Exception as e:
        logging.error(e)
        raise ValueError(e)

    _get_chunks = api.get_chunks(_file.__dict__)

    # upload new
    if _get_chunks["uuid"] == '' or _get_chunks["uploadID"] == '':
        _file.uuid, _file.upload_id = api.new_multipart(_file.__dict__)
        if _get_chunks["uuid"] == '' and _get_chunks["uploadID"] == '':
            upload_chunks = [i for i in range(1, _file.total_chunks_count+1)]
            upload_with_tqdm(_file, api, upload_chunks)
        else:
            msg = f'❌ Upload failed: {_file.filename}` ({cluster}), please contact us. '
            logging.error(msg)
            raise RuntimeError(msg)

    # upload completed
    if _get_chunks["uploaded"] == "1":
        # if _get_chunks.attachID == "0": # 删除数据集记录，未删除文件
        #     api.add_attachments(_file) # current not implemented in swagger api
        if _get_chunks["datasetID"] != "" and _get_chunks["datasetName"] != "":  
            # ?on web js: and file.realName != ""
            msg = f'❌ Upload failed: `{_file.filename}` ({cluster})'\
                  ' already exists, cannot be uploaded again. '
            logging.error(msg)
            raise ValueError(msg)

    # upload continue
    if _get_chunks["uuid"] != '' or _get_chunks["uploadID"] != '':
        _file.uuid, _file.upload_id = _get_chunks["uuid"], _get_chunks["uploadID"]
        continue_index = max([int(i.split('-')[0]) for i in _get_chunks["chunks"].split(',') if i != ''])
        continue_chunks = [i for i in range(continue_index, _file.total_chunks_count+1)]
        upload_with_tqdm(_file, api, continue_chunks)

    # complete upload process
    api.complete_multipart(_file.__dict__)
    _url = f"{api.endpoint.split('/api')[0]}/{repo_id}/datasets"
    msg = f'{logger.get_time()} - 🎉 Successfully uploaded, view on link: {_url}'
    logging.info(msg)
    print(msg)
