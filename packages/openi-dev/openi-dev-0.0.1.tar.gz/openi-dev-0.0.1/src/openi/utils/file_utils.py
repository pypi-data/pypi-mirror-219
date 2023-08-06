import hashlib
import math
import json
from datetime import datetime
from pathlib import Path
from openi.settings import *

def calculateMD5(filepath: str = None) -> str:
        """
        计算文件的完整md5
        :param self.filepath:
        :return:
        """
        m = hashlib.md5()  # 创建md5对象
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                m.update(data)  # 更新md5对象
        return m.hexdigest()  # 返回md5对象

def read_file_chunk(filepath: str = None, start_position: int = 0, chunk_size: int = None):
    with open(filepath, 'rb') as file:
        file.seek(start_position)  # Move the file pointer to the desired start position
        chunk = file.read(chunk_size)  # Read the specified chunk size from the current position
        return chunk

def get_file_chunk(chunk_size: int, filesize: int = 0) -> dict:
    total_chunks_count = math.ceil(filesize / chunk_size)
    # chunks = {i: (i-1)*chunk_size for i in range(total_chunks_count+1)}
    # for chunk_number in range(1, total_chunks_count + 1):
    #     start_position = (chunk_number - 1) * max_chunk_size
    #     chunk_size = filesize - start_position if chunk_number == total_chunks_count else max_chunk_size
    #     chunks[chunk_number] = (start_position, chunk_size)
    return total_chunks_count

def get_token() -> str:
    # if os.name != 'nt':
    #     permissions = os.stat(PATH.TOKEN_PATH).st_mode
    #     if (permissions & 4) or (permissions & 32):
    #         print(
    #             '[WARNING] Your OpenI token is readable by other '
    #             'users on this system! To fix this, you can run ' +
    #             '\'chmod 600 {}\''.format(PATH.TOKEN_PATH))
        
    return json.loads(Path(PATH.TOKEN_PATH).read_text())

def rename_existing_file(filepath):
    path, suffix = os.path.splitext(filepath)
    counter = 0
    filename = "{}({}){}"
    while os.path.exists(filename.format(path, counter, suffix)):
        counter += 1
    new = filename.format(path, counter, suffix)

    return new
