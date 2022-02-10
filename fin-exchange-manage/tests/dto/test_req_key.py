from rest.proxy_controller import PayloadReqKey


def test_clean_default_keys():
    p = {
        PayloadReqKey.apiKey.value: 123,
        PayloadReqKey.name.value: 'dd'
    }
    np = PayloadReqKey.clean_default_keys(p)
    print(np)
