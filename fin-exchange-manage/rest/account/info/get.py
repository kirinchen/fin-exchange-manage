from typing import Any


def run( payload: dict) -> Any:
    result: AccountInformation = client.get_account_information()
    result.assets = None
    result.positions = None
    return result.__dict__
