#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
加密
"""
import base64
from M2Crypto import EVP
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature.PKCS1_v1_5 import PKCS115_SigScheme


def evp_encrypt(key, data, ivector=None, alg="aes_128_cbc"):
    """
    加密
    :param str key: 密钥
    :param str data: 明文
    :param str ivector: 初始化向量
    :param str alg: 加密算法
    :return: 密文
    """
    if not ivector:
        ivector = key
    cipher = EVP.Cipher(alg, key, ivector, 1)
    encryptext = cipher.update(data)
    encryptext += cipher.final()
    return encryptext


def evp_decrypt(key, data, ivector=None, alg="aes_128_cbc"):
    """
    解密
    :param str key: 密钥
    :param str data: 密文
    :param str ivector: 初始化向量
    :param str alg: 加密算法
    :return: 明文
    """
    if not ivector:
        ivector = key
    cipher = EVP.Cipher(alg, key, ivector, 0)
    plaintext = cipher.update(data)
    plaintext += cipher.final()
    return plaintext


def des_encrypt(key, data, ivector=None):
    """
    DES加密
    :param key: DES密钥, 必须8位
    :param data: 明文
    :param ivector: 初始化向量
    :param :return: 密文
    """
    if not ivector:
        ivector = key
    cipher = EVP.Cipher("des_cbc", key, ivector, 1)
    encryptext = cipher.update(data)
    encryptext += cipher.final()
    return encryptext


def des_decrypt(key, data, ivector=None):
    """
    DES解密
    :param key: DES密钥, 必须8位
    :param data: 密文
    :param ivector: 初始化向量
    :param :return: 明文
    """
    if not ivector:
        ivector = key
    cipher = EVP.Cipher("des_cbc", key, ivector, 0)
    plaintext = cipher.update(data)
    plaintext += cipher.final()
    return plaintext


def generate_signature(private_key, data):
    """
    生成签名
    :param private_key: 私钥
    :param data: 待签名数据
    :param :return: base64编码的签名串
    """
    str_data = "&".join(["%s=%s" % (k, v) for k, v in sorted(data.items()) if k != "sign" and v != ""])
    h = SHA.new(str_data)
    scheme = PKCS115_SigScheme(RSA.importKey(private_key))
    return base64.b64encode(scheme.sign(h))


def verify_signature(public_key, data):
    """
    验证签名
    :param data: 待验签的数据, 字典形式
    :param signature: 签名数据
    :param :return: True or False
    """
    str_data = "&".join(["%s=%s" % (k, v) for k, v in sorted(data.items()) if k != "sign" and v != ""])
    h = SHA.new(str_data)
    signature = base64.b64decode(data["sign"])
    sign_scheme = PKCS115_SigScheme(RSA.importKey(public_key))
    return sign_scheme.verify(h, signature)


def verify_signature_raw(public_key, str_data, sign):
    """
    验证签名
    :param data: 待验签的数据, 字符串
    :param signature: 签名数据
    :param :return: True or False
    """
    h = SHA.new(str_data)
    signature = base64.b64decode(sign)
    sign_scheme = PKCS115_SigScheme(RSA.importKey(public_key))
    return sign_scheme.verify(h, signature)


def crypt_encrypt(alg, key, data, ivector=None):
    """
    加密
    :param alg: 加密算法
    :param key: DES密钥, 必须8位
    :param data: 明文
    :param ivector: 初始化向量
    :param :return: 密文
    """
    if not ivector:
        ivector = key
    cipher = EVP.Cipher(alg, key, ivector, 1)
    encryptext = cipher.update(data)
    encryptext += cipher.final()
    return encryptext


def crypt_decrypt(alg, key, data, ivector=None):
    """
    加密
    :param alg: 加密算法
    :param key: DES密钥, 必须8位
    :param data: 明文
    :param ivector: 初始化向量
    :param :return: 密文
    """
    if not ivector:
        ivector = key
    cipher = EVP.Cipher(alg, key, ivector, 0)
    encryptext = cipher.update(data)
    encryptext += cipher.final()
    return encryptext


def rsa_sign_raw(private_key, str_data):
    """
    生成签名
    :param private_key: 私钥
    :param data: 待签名字符串数据
    :return: True or False
    """
    h = SHA.new(str_data)
    scheme = PKCS115_SigScheme(RSA.importKey(private_key))
    return base64.b64encode(scheme.sign(h))


def rsa_verify_raw(public_key, str_data, sign):
    """
    验证签名
    :param data: 待验签的数据, 字符串
    :param signature: 签名数据
    :return: True or False
    """
    h = SHA.new(str_data)
    signature = base64.b64decode(sign)
    sign_scheme = PKCS115_SigScheme(RSA.importKey(public_key))
    return sign_scheme.verify(h, signature)

