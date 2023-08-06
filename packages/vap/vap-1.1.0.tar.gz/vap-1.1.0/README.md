# vap - [Verify Apple Postback](https://developer.apple.com/documentation/storekit/skadnetwork/verifying_an_install-validation_postback#3599761)

[![Slava Ukraini](https://img.shields.io/badge/Slava-Ukraini-FFD500?style=flat&labelColor=005BBB)](https://bank.gov.ua/en/news/all/natsionalniy-bank-vidkriv-spetsrahunok-dlya-zboru-koshtiv-na-potrebi-armiyi) [![Support Ukraine](https://img.shields.io/badge/Support-Ukraine-FFD500?style=flat&labelColor=005BBB)](https://opensource.fb.com/support-ukraine)

[![Python versions](https://img.shields.io/pypi/pyversions/vap.svg?logo=python&logoColor=81B441)](https://docs.python.org/3/)
[![Code size](https://img.shields.io/github/languages/code-size/d-ganchar/vap.svg?logo=Dropbox&logoColor=ACD2F6)](https://github.com/d-ganchar/vap/tree/master/vap)
[![PyPI version](https://img.shields.io/pypi/v/vap.svg?logo=pypi&logoColor=FFE200)](https://pypi.org/project/vap/)
[![Build Status](https://api.travis-ci.com/d-ganchar/vap.svg?branch=master)](https://www.travis-ci.com/github/d-ganchar/vap)

#### How to install:
```bash
$ pip install vap
```

#### How to use:
```bash
$ vap verify '{"version": "4.0", "ad-network-id": "com.example", "source-identifier": "39", "app-id": 525463029, "transaction-id": "6aafb7a5-0170-41b5-bbe4-fe71dedf1e31", "redownload": false, "source-domain": "example.com", "fidelity-type": 1, "did-win": true, "coarse-conversion-value": "high", "postback-sequence-index": 0, "attribution-signature": "MEUCIQD4rX6eh38qEhuUKHdap345UbmlzA7KEZ1bhWZuYM8MJwIgMnyiiZe6heabDkGwOaKBYrUXQhKtF3P/ERHqkR/XpuA="}'
# 1
```

```python
from vap.verifier import verify_postback

postback = {
    'version': '4.0',
    'ad-network-id': 'com.example',
    'source-identifier': '5239',
    'app-id': 525463029,
    'transaction-id': '6aafb7a5-0170-41b5-bbe4-fe71dedf1e30',
    'redownload': False,
    'source-domain': 'example.com',
    'fidelity-type': 1,
    'did-win': True,
    'conversion-value': 63,
    'postback-sequence-index': 0,
    'attribution-signature': 'MEUCIGRmSMrqedNu6uaHyhVcifs118R5z/AB6cvRaKrRRHWRAiEAv96ne3dKQ5kJpbsfk4eYiePmr'
                             'ZUU6sQmo+7zfP/1Bxo=',
}

print(verify_postback(postback)) # True
```

[Supported versions](https://github.com/d-ganchar/vap/blob/master/tests/test_verifier.py#L10)