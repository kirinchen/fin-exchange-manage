import traceback

from infra import database
from service import order_builder
from service.order_builder import BaseOrderBuilder, LoadDataCheck
from service.position_fuse import fuse_builder
from service.position_fuse.fuse_builder import BaseFuseBuilder
from utils import comm_utils


def run(payload: dict) -> dict:
    try:
        with database.session_scope() as session:
            fb: BaseFuseBuilder = fuse_builder.gen_fuse_builder(session, payload)
            return comm_utils.to_dict(fb.fuse())
    except Exception as e:  # work on python 3.x
        return {
            'type': str(type(e)),
            'msg': str(e),
            'traceback': traceback.format_exc()
        }
