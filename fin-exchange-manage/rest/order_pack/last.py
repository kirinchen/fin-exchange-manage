import exchange
from dto import order_dto
from infra import database
from infra.enums import PayloadReqKey
from service.order_pack_dao import OrderPackDao
from utils import comm_utils


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        ex = PayloadReqKey.exchange.get_val(payload)
        order_pack_dao: OrderPackDao = exchange.gen_impl_obj(exchange_name=ex, session=session,
                                                             clazz=OrderPackDao,**payload)
        PayloadReqKey.clean_default_keys(payload)
        filter_map: dict = payload.get('filter_map')
        ans = dict()
        for k, v in filter_map.items():
            ans[k] = fetch_one(v, order_pack_dao)
        return ans


def fetch_one(f_dict: dict, order_pack_dao: OrderPackDao) -> object:
    (order_pack, orders) = order_pack_dao.last(f_dict)
    if not order_pack:
        return None
    return {
        "orderPack": order_pack.to_dict(),
        "orders": comm_utils.to_dict([order_dto.convert_entity_to_dto(o) for o in orders])
    }
