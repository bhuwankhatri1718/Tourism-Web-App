import hashlib
import hmac
import base64
import json

# eSewa's official published TEST/sandbox merchant credentials.
# Public, free to use, no registration required, no real money moves.
ESEWA_MERCHANT_CODE = "EPAYTEST"
ESEWA_SECRET_KEY = "8gBm/:&EnhH.1/q"
ESEWA_FORM_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"


def generate_signature(total_amount, transaction_uuid, product_code=ESEWA_MERCHANT_CODE):
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    hmac_obj = hmac.new(ESEWA_SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode('utf-8')


def decode_response(data_param):
    decoded = base64.b64decode(data_param).decode('utf-8')
    return json.loads(decoded)