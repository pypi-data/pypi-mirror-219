import zlib
import torch
from io import BytesIO
from websockets.sync.client import connect

from .logger import *

Port = 65532
RenderType = 'Provider'
TypeHeader = 'X-Client-Type'
Headers = {TypeHeader: RenderType}

__all__ = ['send']


def get_bytes(args) -> bytes:
    buffer = BytesIO()
    torch.save(args, buffer, _use_new_zipfile_serialization=False)
    buffer = zlib.compress(buffer.getvalue())

    log_info(f'正在创建渲染请求,包大小: {format_capacity(buffer)}')
    return buffer


def send(method='visualize_point_cloud', **args):
    if len(args) == 0:
        raise ValueError('渲染需要至少一个有效的参数')

    args['method'] = method
    message = get_bytes(args)

    with connect(f'ws://localhost:{Port}', additional_headers=Headers, max_size=500*1024*1024) as socket:
        socket.send(message)
        socket.close(code=1000, reason='主动断开')
        log_info('渲染请求创建成功,请在渲染终端上查看效果')
