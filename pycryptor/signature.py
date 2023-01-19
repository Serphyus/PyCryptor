from typing import Tuple

from Crypto.Cipher import AES


def create_signature(aes_key: bytes, data: bytes) -> Tuple[bytes, bytes, bytes]:
	cipher = AES.new(aes_key, AES.MODE_EAX)
	ciphertext, tag = cipher.encrypt_and_digest(data)

	return cipher.nonce, tag, ciphertext


def verify_signature(aes_key: bytes, nonce: bytes, tag: bytes, data: bytes) -> bytes:
	cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
	data = cipher.decrypt_and_verify(data, tag)

	return data