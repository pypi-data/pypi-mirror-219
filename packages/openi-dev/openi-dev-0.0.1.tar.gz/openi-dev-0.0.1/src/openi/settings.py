import os
import textwrap

"""
File PATHs
"""
class PATH(object):
    OPENI_FOLDER = os.path.join(os.path.expanduser('~'), ".openi") # os.path.expanduser('~'), os.getcwd()
    TOKEN_PATH = os.path.join(OPENI_FOLDER, "token.json") 
    SAVE_PATH = os.path.join(os.getcwd(), "dataset")
    LOG_PATH = os.path.join(OPENI_FOLDER, "openi.log")
    TOKEN_PATTERN = r"^[0-9a-fA-F]{40}$"

"""
API
"""
class API(object):
    ENDPOINT = "https://openi.pcl.ac.cn"
    VERSION = "/api/v1"

"""
Datasets
"""
class DATASET(object):
    SOTRAGE_TYPE = {"GPU": 0, "NPU": 1}
    MAX_FILE_SIZE_GB = 200
    SMALL_FILE_CHUNK_SIZE = 1024 * 1024 * 8
    LARGE_FILE_CHUNK_SIZE = 1024 * 1024 * 64

    MAX_CHUNKS = 10000
    MAX_FILE_SIZE = 1024 * 1024 * 1024 * MAX_FILE_SIZE_GB
    SMALL_FILE_LIMIT = 1024 * 1024 * 8 * MAX_CHUNKS


"""
CLI help 
"""
class CLI(object):

    # main help page
    banner = '启智AI协作社区命令行工具 OpenI command line tool'

    usage = 'openi [commands] [<args>] [-h]'
    command_login = '命令行界面登录，或者使用`--token`参数直接登录'
    command_logout = '登出当前用户并删除token文件'
    command_whoami = '查询当前登录用户信息'
    command_dataset = '{upload,download} 上传/下载启智AI协作平台的数据集 '

    # Login
    login_usage = 'openi login [--token] [--endpoint] [-h]'
    param_token = '选填: 从启智AI协作平台生成的`令牌(Access Token)`'
    param_endpoint = '选填: 仅内部使用.'

    # Dataset
    dataset_choices = ['upload', 'download']
    dataset_usage = 'openi dataset(d) {upload,download} [<args>] [-h]'

    command_dataset_upload = '上传数据集文件，需指定文件名,仓库路径及存储类型'
    dataset_upload_help = '下载数据集文件, openi dataset upload -h 查看更多说明'
    dataset_upload_usage = 'openi dataset(d) upload [file] [repo_id] [cluster] [-h]'
    dataset_upload_param_file = '本地文件名称，包含文件路径'
    dataset_upload_param_repo_id = '所在仓库路径，格式为`拥有者/仓库名`，登录用户需要拥有此仓库权限'
    dataset_upload_param_cluster = '文件的存储集群，不区分大小写，默认为`NPU`'
    dataset_upload_epilog = textwrap.dedent(
        """
        用法说明：\n
        登录用户为user1，并且为user2/repo2仓库的协作者 \n
        用法一: openi dataset upload data1.zip user1/repo1 gpu
        上传本地文件`data1.zip`到repo1仓库数据集，存储类型为GPU \n
        用法二: openi d upload localDir/data2.zip user2/repo2 
        上传本地文件`./localDir/data2.zip`到协作仓库user2/repo2，存储类型为NPU \n
        """)

    command_dataset_download = '下载数据集文件，需指定文件名,仓库路径及存储类型'
    dataset_download_help = '下载数据集文件, openi dataset download -h 查看更多说明'
    dataset_download_usage = 'openi dataset(d) download ' \
                             '[file] [repo_id] [cluster] ' \
                             '[-p save_path] [-h]'
    dataset_download_param_file = '网页端数据集文件名称，只能下载`.zip`或`.tar.gz`格式的文件'
    dataset_download_param_save_path = '选填: 本地的保存路径，默认为在当前路径下创建`dataset`目录'
    dataset_download_epilog = textwrap.dedent(
        """
        用法说明： \n
        登录用户为user1，并且为user2/repo2仓库的协作者\n
        用法一: openi dataset download data1.zip user1/repo1 gpu -p /downloads
        从repo1仓库下载`data1.zip`(GPU)数据集文件，并存到本地`/downloads/data1.zip`\n
        用法二: openi d download data2.zip user2/repo2
        从协作仓库user2/repo2下载`data2.zip`(NPU)数据集文件，并存到本地`./dataset/data2.zip`\n
        """)

    command_dataset_link = '通过链接下载数据集文件, 下载链接在网页端数据集文件列表取得，更多->复制下载链接'
    dataset_link_help = '通过链接下载数据集文件, openi dataset link -h 查看更多说明'
    dataset_link_usage = 'openi dataset(d) link [link] [--download] [-p save_path] [-h]'
    dataset_link_param_link = '网页端复制的数据集链接'
    dataset_link_param_link_only = '选填: bool参数无需填写取值，添加即为`True`，区分是否仅获取下载链接'
    dataset_link_param_save_path = '选填: 本地的保存路径，默认为在当前路径下创建`dataset`目录，填写`--link_only`时失效'
    dataset_link_epilog = textwrap.dedent(
        """
        用法说明：\n
        用法一: openi dataset link https://openi.pcl.ac.cn/attachments/c0b804a9-7cea-4d43-a757-d5f4df2b4bda?type=0 -p /downloads \n
        用法二: openi d link https://openi.pcl.ac.cn/attachments/c0b804a9-7cea-4d43-a757-d5f4df2b4bda?type=0 --link_only\n
        """)

    # General params
    param_default = 'TODO'

