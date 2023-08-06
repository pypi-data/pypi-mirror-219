from io import BytesIO
import base64
from PIL import Image
from datetime import datetime

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


