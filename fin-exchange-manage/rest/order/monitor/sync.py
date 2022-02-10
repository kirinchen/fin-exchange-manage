import exchange
from infra import database
from rest.proxy_controller import PayloadReqKey
from service.sync_cron import SyncCron


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        ex = PayloadReqKey.exchange.get_val(payload)
        sync_cron: SyncCron = exchange.gen_impl_obj(exchange_name=ex, session=session,
                                                    clazz=SyncCron,**payload)

        return sync_cron.sync_orders(prd_name=payload.get('prd_name'))
