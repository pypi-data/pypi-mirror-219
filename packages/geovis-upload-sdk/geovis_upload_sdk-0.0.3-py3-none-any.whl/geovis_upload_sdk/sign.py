import hmac
import base64
import hashlib


def hmacSHA256(message, key):
    hmacKey = base64.b64decode(key)
    signature = hmac.new(hmacKey, message.encode(), hashlib.sha256).digest()
    signatureStr = base64.b64encode(signature).decode("utf-8")
    return signatureStr


def computeBufferHash(buffer):
    md5_hash = hashlib.md5()
    md5_hash.update(buffer)
    encrypted_data = md5_hash.hexdigest()
    return encrypted_data
