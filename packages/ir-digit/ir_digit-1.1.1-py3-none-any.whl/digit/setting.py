import os

# 根目录
ROOT_PATH = os.path.expanduser("~")
# ROOT_PATH = "D:\\"
# 缓存文件夹
CACHE_PATH = os.path.join(ROOT_PATH, "digit")

# Digit Web接口
## test
# INTERFACE_PATH = 'http://127.0.0.1:8000'
## product
INTERFACE_PATH = 'http://124.70.200.79:10101'


DATA_STORAGE_TYPE_DEFAULT = 11
DATA_STORAGE_TYPE = {
    # Git仓库
    11: "Gitee",
    12: "Github",
    13: "其他托管",

    # 网络云盘
    21: "百度网盘",
    22: "阿里云盘",
    23: "坚果云网盘",
    24: "谷歌网盘",
    25: "其他网盘",

    # 实验室服务器
    31: "数据服务器",
    32: "GPU服务器",
    33: "华为服务器",
    34: "其他服务器"
}

DATA_DATA_TYPE_DEFAULT = 2
DATA_DATA_TYPE = {
    0: "Only Dataset",
    1: "Only Code",
    2: "Dataset & Code"
}

DATA_LANGUAGE_DEFAULT = 0
DATA_LANGUAGE = {
    0: 'English',
    1: 'Chinese',
    2: 'English & Chinese',
    3: 'Other'
}

DATA_TASK_TYPE_DEFAULT = 31
DATA_TASK_TYPE = {
    # "Multimodal"
    11: 'Feature Extraction',
    12: 'Text-to-Image',
    13: 'Image-to-Text',
    14: 'Text-to-Video',
    15: 'Visual Question Answering',
    16: 'Document Question Answering',
    17: 'Graph Machine Learning',

    # "Computer Vision"
    21: 'Depth Estimation',
    22: 'Image Classification',
    23: 'Object Detection',
    24: 'Image Segmentation',
    25: 'Image-to-Image',
    26: 'Unconditional Image Generation',
    27: 'Video Classification',
    28: 'Zero-Shot Image Classification',

    # "Natural Language Processing"
    31: 'Text Classification',
    32: 'Token Classification',
    33: 'Table Question Answering',
    34: 'Question Answering',
    35: 'Zero-Shot Classification',
    36: 'Translation',
    37: 'Summarization',
    38: 'Conversational',
    39: 'Text Generation',
    310: 'Text2Text Generation',
    311: 'Fill-Mask',
    312: 'Sentence Similarity',

    # "Audio"
    41: 'Text-to-Speech',
    42: 'Automatic Speech Recognition',
    43: 'Audio-to-Audio',
    44: 'Audio Classification',

    # "Tabular"
    45: 'Voice Activity Detection',
    51: 'Tabular Classification',
    52: 'Tabular Regression',
    61: 'Reinforcement Learning',
    62: 'Robotics',
    # other
    0: 'other'
}
