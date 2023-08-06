import argparse
import json
from json import JSONDecodeError

import pkg_resources
import sys

from .verifier import verify_postback


def run():
    parser = argparse.ArgumentParser(
        prog='vap',
        description='postback Apple verifier',
        epilog=f'vap v{pkg_resources.get_distribution("vap").version}',
    )

    subparsers = parser.add_subparsers(help='verify apple postback')
    postback = subparsers.add_parser('verify', help="""
        vap verify '{"version": "4.0", ...}'
    """)

    postback.add_argument('postback', help="""
    json postback: {
        "version": "4.0",
        "ad-network-id": "com.example",
        "source-identifier": "39",
        "app-id": 525463029,
        "transaction-id": "6aafb7a5-0170-41b5-bbe4-fe71dedf1e31",
        "redownload": false,
        "source-domain": "example.com",
        "fidelity-type": 1,
        "did-win": true,
        "coarse-conversion-value": "high",
        "postback-sequence-index": 0,
        "attribution-signature": "MEUCIQD4rX6eh38qEhuUKHdap345UbmlzA7KEZ1bhWZuYM8MJwIgMnyiiZe6heabDkGwOaKBYrUXQhKtF3P/ERHqkR/XpuA="
    }
    """)

    params = parser.parse_args(sys.argv[1:])

    try:
        postback = json.loads(params.postback)
    except JSONDecodeError as error:
        print(f'JSON parse error. {error}')
        exit(1)

    print(int(verify_postback(postback)))
