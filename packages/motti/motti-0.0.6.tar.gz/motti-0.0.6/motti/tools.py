from io import BytesIO
import base64
from PIL import Image
from datetime import datetime
import os
from typing import Optional, Union
from pathlib import Path


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

def project_dir_with(project_dir="."):
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
