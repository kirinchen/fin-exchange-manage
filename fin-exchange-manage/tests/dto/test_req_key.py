from infra.enums import PayloadReqKey


def test_clean_default_keys():
    p = {
        PayloadReqKey.apiKey.value: 123,
        PayloadReqKey.name.value: 'dd'
    }
    np = PayloadReqKey.clean_default_keys(p)
    print(np)
