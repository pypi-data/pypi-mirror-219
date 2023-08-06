from io import BytesIO
import base64
from PIL import Image
from datetime import datetime
import os
from typing import Optional, Union
from pathlib import Path
import argparse
import yaml
from dataclasses import dataclass, asdict
import torch
import numpy as np
import random

def pil2str(x):
    buffer = BytesIO()
    x.save(buffer, format='PNG')
    b64 = base64.b64encode(buffer.getvalue())
    res = str(b64, 'utf-8')
    return res

def str2pil(s):
    b64 = base64.b64decode(s.encode('utf-8'))
    return Image.open(BytesIO(b64))

def get_datetime():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def init_project_dir_with(project_dir="."):
    def f(*args, **kwargs):
        return os.path.join(project_dir, *args, **kwargs)
    return f

def is_abs_path(path: Union[Path, str]):
    if isinstance(path, Path):
        return path.is_absolute()
    elif isinstance(path, str):
        return os.path.isabs(path)
    else:
        raise NotImplementedError 
        return False

def load_yaml(path):
    return yaml.safe_load(open(path, 'r'))

def load_namespace(path):
    D = load_yaml(path)
    return argparse.Namespace(**D)

def seed_everything(seed):
    torch.manual_seed(seed)       # Current CPU
    torch.cuda.manual_seed(seed)  # Current GPU
    np.random.seed(seed)          # Numpy module
    random.seed(seed)             # Python random module
    torch.backends.cudnn.benchmark = False    # Close optimization
    torch.backends.cudnn.deterministic = True # Close optimization
    # torch.cuda.manual_seed_all(seed) # All GPU (Optional)
