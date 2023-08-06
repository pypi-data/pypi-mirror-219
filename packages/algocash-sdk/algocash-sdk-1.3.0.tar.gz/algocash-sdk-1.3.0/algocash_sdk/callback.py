from __future__ import absolute_import

from algocash_sdk.api_client import ApiClient
import hashlib
import json
import hmac

class Callback():
    def construct_callback(self, payload, sig_header, secret):
        signature = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
        if sig_header != signature:
            raise SignatureVerificationException('Signature is invalid')
        api_client = ApiClient()
        return api_client.deserialize(payload, 'CallbackPayload', False)
    
class SignatureVerificationException(Exception):

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return self.message