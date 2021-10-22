from service import order_builder
from service.order_builder import BaseOrderBuilder, LoadDataCheck
from utils import comm_utils


def run(payload: dict) -> dict:
    ob: BaseOrderBuilder = order_builder.gen_order_builder(payload)
    check_result: LoadDataCheck = ob.load_data()
    if not check_result.success:
        return comm_utils.to_dict(check_result)
    return comm_utils.to_dict(order_builder.post())
