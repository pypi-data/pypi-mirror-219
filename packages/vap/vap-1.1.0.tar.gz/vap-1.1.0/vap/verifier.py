import base64 as b64
from typing import Tuple, Union

from fastecdsa import curve as fe_curve, keys as fe_keys, ecdsa as fe_ecdsa
from fastecdsa.encoding import der as fe_der, pem as fe_pem
from fastecdsa.ecdsa import MsgTypes, Curve
from hashlib import sha256

from .errors import VapError


"""
Apple’s NIST P-256 public key that you use to verify signatures for versions 2.1 and later.

see: https://developer.apple.com/documentation/storekit/skadnetwork/verifying_an_install-validation_postback#3599761
"""
_APPLE_PUB_KEY = '\n-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWdp8GPcGqmhgzEFj9Z2nSpQVddayaPe4' \
                 'FMzqM9wib1+aHaaIzoHoLN9zW4K8y4SPykE3YVK3sVqW6Af0lfx3gg==\n-----END PUBLIC KEY-----'


class _EcdsaWrapper:
    """
    see: https://github.com/singular-labs/Singular-SKAdNetwork-App/blob/master/skadnetwork-server/ecdsa_wrapper.py
    see: https://stackoverflow.com/questions/64496534/how-to-verify-a-postback-with-skadnetwork-apple
    """
    CURVEP192 = fe_curve.P192
    CURVEP256 = fe_curve.P256
    CURVE = CURVEP256
    SIGRAW = 0
    SIGB64 = 1
    SIGHEX = 2
    SIGFMT = SIGB64
    HASH = sha256

    def __init__(self, pem: str = None):
        if pem is None:
            self._key, self._pubkey = fe_keys.gen_keypair(self.CURVE)
            return

        self._key, self._pubkey = fe_pem.PEMEncoder.decode_private_key(pem.strip())
        if self._pubkey is None:
            self._pubkey = fe_keys.get_public_key(self._key, self.CURVE)

    def __str__(self):
        if self._key is not None:
            return str(self._key)
        return str(self._pubkey)

    def export(self):
        if self._key is not None:
            return fe_keys.export_key(self._key, curve=self.CURVE)
        return fe_keys.export_key(self._pubkey, curve=self.CURVE)

    @property
    def key(self):
        return self.export()

    @property
    def pubkey(self):
        return fe_keys.export_key(self._pubkey, curve=self.CURVE)

    def sign(self, message: MsgTypes, sig_fmt: int = None, curve: Curve = None):
        if sig_fmt is None:
            sig_fmt = self.SIGFMT
        if curve is None:
            curve = self.CURVE
        if self._key is None:
            return None

        return self._sig_encode(fe_ecdsa.sign(message, self._key, curve=curve, hashfunc=self.HASH), sig_fmt)

    def _sig_encode(self, sigrs: Tuple[int, int], sig_fmt: int = None):
        if sig_fmt is None:
            sig_fmt = self.SIGFMT

        sigr, sigs = sigrs
        sig = fe_der.DEREncoder.encode_signature(sigr, sigs)

        if sig_fmt == self.SIGRAW:
            return sig
        elif sig_fmt == self.SIGB64:
            return b64.b64encode(sig)
        elif sig_fmt == self.SIGHEX:
            return sig.hex()
        else:
            raise VapError(f'unknown signature format {sig_fmt}')

    def _sig_decode(self, sig: Union[str, bytes, bytearray], sig_fmt: int = None) -> (int, int):
        if sig_fmt is None:
            sig_fmt = self.SIGFMT

        if sig_fmt == self.SIGRAW:
            return fe_der.DEREncoder.decode_signature(sig)
        elif sig_fmt == self.SIGB64:
            return fe_der.DEREncoder.decode_signature(b64.b64decode(sig))
        elif sig_fmt == self.SIGHEX:
            return fe_der.DEREncoder.decode_signature(bytes.fromhex(sig))

    def verify(self, message: MsgTypes, sig: Union[str, bytes, bytearray], sig_fmt: int = None) -> bool:
        if sig_fmt is None:
            sig_fmt = self.SIGFMT

        sigr, sigs = self._sig_decode(sig, sig_fmt)

        try:
            return fe_ecdsa.verify((sigr, sigs), message, self._pubkey, curve=self.CURVE, hashfunc=self.HASH)
        except:
            return False


_ecdsa_wrapper = _EcdsaWrapper(_APPLE_PUB_KEY)


def verify_postback(postback: dict) -> bool:
    version = postback['version']
    float_version = float(version)
    if float_version < 2.1 or float_version >= 5:
        return False

    campaign_id = str(postback.get('campaign-id'))
    app_id = str(postback['app-id'])
    redownload = str(postback.get('redownload')).lower()
    ad_network_id = postback['ad-network-id']
    transaction_id = postback['transaction-id']
    source_identifier = postback.get('source-identifier') or ''
    fidelity_type = str(postback.get('fidelity-type'))
    did_win = str(postback.get('did-win')).lower()
    source_domain = postback.get('source-domain') or ''
    postback_sequence_index = str(postback.get('postback-sequence-index'))
    source_app_id = postback.get('source-app-id')

    if source_app_id is not None:
        if float_version < 3:
            source_app_id = str(source_app_id) if isinstance(source_app_id, int) else ''
        else:
            source_app_id = str(postback['source-app-id']) if postback['source-app-id'] > 0 else ''

    if 4 <= float_version < 5:
        if source_app_id:
            message_items = [version, ad_network_id, source_identifier, app_id, transaction_id, redownload,
                             source_app_id, fidelity_type, did_win, postback_sequence_index]
        elif source_domain:
            message_items = [version, ad_network_id, source_identifier, app_id, transaction_id, redownload,
                             source_domain, fidelity_type, did_win, postback_sequence_index]
        else:
            message_items = [version, ad_network_id, source_identifier, app_id, transaction_id, redownload,
                             fidelity_type, did_win, postback_sequence_index]
    elif 3 <= float_version < 4:
        if source_app_id:
            message_items = [version, ad_network_id, campaign_id, app_id, transaction_id, redownload, source_app_id,
                             fidelity_type, did_win]
        else:
            message_items = [version, ad_network_id, campaign_id, app_id, transaction_id, redownload, fidelity_type,
                             did_win]
    else:
        message_items = [version, ad_network_id, campaign_id, app_id, transaction_id, redownload, source_app_id]

    message = u'\u2063'.join(message_items)
    return _ecdsa_wrapper.verify(message, postback['attribution-signature'])
