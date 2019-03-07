#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
银联移动支付
"""
import os
import base64
import urllib
import urllib2
import logging
import hashlib
import urlparse
import datetime
from OpenSSL import crypto


RESP_CODE_SUCC = "00"  # 成功应答码


def parse_qsl_data(post_data):
    """
    解析原始数据
    :param string post_data: 待解析的数据
    """
    param = dict(urlparse.parse_qsl(post_data))
    param["signature"] = param["signature"].replace(" ", "+")
    param = UnionpayAcpClient._filter_param(param)
    return param


class UnionpayAcpClient(object):
    """
    银联的控件支付
    """
    def __init__(self, conf):
        """
        初始化配置
        :param dict conf:{
            "mer_id":"商户ID",
            "back_notify_url":"后台通知地址",
            "front_notify_url":"前台通知地址, 对控件支付来说, 没有用",
            "app_trans_req":"app交易地址",
            "sign_cert_path":"签名证书路径",
            "sign_cert_pwd":"签名证书密码",
            "verify_cert_path":"验签证书路径"
        }
        """
        self.conf = conf
        self.pkcs12 = self._load_pkcs12()
        self.pubkey = self._load_pubkey_cert()
        self.pubkey_dict = self._load_pubkey_dict()

    def _load_pkcs12(self):
        """
        读取商户自己的签名证书
        """
        pkbuffer = open(self.conf["sign_cert_path"]).read()
        return crypto.load_pkcs12(pkbuffer, self.conf["sign_cert_pwd"])

    def get_sign_cert_id(self):
        """
        读取签名证书的ID
        """
        return self.pkcs12.get_certificate().get_serial_number()

    def _load_pubkey_cert(self):
        """
        读取银联的验签公钥
        """
        cert_path = self.conf["verify_cert_path"]
        file_path = os.path.join(cert_path, "UpopRsaCert.cer")
        with open(file_path) as fobj:
            content = fobj.read()
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, content)
        return cert

    def _load_pubkey_dict(self):
        """
        读取银联的公钥
        """
        cert_path = self.conf["verify_cert_path"]
        cert_dict = {}
        for i in os.listdir(cert_path):
            file_path = os.path.join(cert_path, i)
            if not os.path.isfile(file_path):
                continue
            if not os.path.splitext(i)[1] == ".cer":
                continue

            with open(file_path) as fobj:
                content = fobj.read()
                cert = crypto.load_certificate(crypto.FILETYPE_PEM, content)
                cert_dict[cert.get_serial_number()] = cert

        return cert_dict

    @staticmethod
    def _filter_param(param):
        """
        过滤参数
        """
        result = {}
        for k in param:
            if k in ("signature", ):
                continue
            result[k] = param[k]
        return result

    def _build_signature(self, param):
        """
        构造签名
        """
        param = self._filter_param(param)
        temp_str, param_keys = "", param.keys()
        for k in sorted(param_keys):
            temp_str += "%s=%s&" % (k, param[k])
        temp_str = temp_str[:-1]
        temp_str = hashlib.sha1(temp_str).hexdigest()
        signature = crypto.sign(self.pkcs12.get_privatekey(), temp_str, "sha1")
        return base64.b64encode(signature)

    def _verify_signature(self, post_data):
        """
        校验响应内容
        :param string post_data: 银联返回数据
        :return: 是否验证通过
        """
        # TODO: 银联SB, 回传的数据都没有经过URI_ENCODE
        param = dict(urlparse.parse_qsl(post_data))
        param["signature"] = param["signature"].replace(" ", "+")

        # 公钥
        cert_id = int(param["certId"])
        if cert_id not in self.pubkey_dict:
            logging.error("certid %s (%s) not exist", cert_id, param)
            return False, None

        pub_x509 = self.pubkey_dict[cert_id]

        # 构造带签名字符串
        signature = base64.b64decode(param["signature"])
        param = self._filter_param(param)
        temp_str, param_keys = "", param.keys()
        for k in sorted(param_keys):
            temp_str += "%s=%s&" % (k, param[k])
        temp_str = hashlib.sha1(temp_str[:-1]).hexdigest()
        try:
            crypto.verify(pub_x509, signature, temp_str, "sha1")
            return True, param
        except crypto.Error:
            logging.error("fail to verify signature:%s", param, exc_info=True)
            return False, None

    @staticmethod
    def send_post(url, data):
        """
        发送POST请求
        """
        resp = urllib2.urlopen(url, data, timeout=10).read()
        return resp

    def create_trade(self, out_trade_no, total_fee, body):
        """
        创建移动支付交易请求数据
        :param string out_trade_no: 交易号(在商户系统中唯一)
        :param int total_fee: 商品价格, 单位: RMB－分
        :param body: 商品描述
        :return: 是否验证通过, {
            "tn":交易流水号,
            "respCode":响应码,
            "respMsg":响应信息,
        }
        """
        now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        param = {
            "version":"5.0.0",                        # 版本号
            "encoding":"utf-8",                       # 编码方式
            "certId":self.get_sign_cert_id(),         # 证书ID
            "txnType":"01",                           # 交易类型
            "txnSubType":"01",                        # 交易子类
            "bizType":"000201",                       # 业务类型
            "frontUrl":self.conf["front_notify_url"], # 前台通知地址，控件接入的时候不会起作用
            "backUrl": self.conf["back_notify_url"],  # 后台通知地址
            "signMethod":"01",                        # 签名方法
            "channelType":"08",                       # 渠道类型, 07-PC, 08-手机
            "accessType":"0",                         # 接入类型
            "merId":self.conf["mer_id"],              # 商户代码，请改自己的商户号
            "orderId":out_trade_no,                   # 商户订单, 8-40位数字字母
            "txnTime":now_str,                        # 订单发送时间
            "txnAmt":total_fee,                       # 交易金额，单位分
            "currencyCode":"156",                     # 交易币种
            "orderDesc":body,                         # 订单描述，可不上送，上送时控件中会显示该信息
            "reqReserved":"zkfc",                     # 请求方保留域, 透传字段，查询、通知中会原样出现
        }
        param["signature"] = self._build_signature(param)
        data = urllib.urlencode(param)
        response = self.send_post(self.conf["app_trans_req"], data)
        is_ok, result = self._verify_signature(response)
        if is_ok and result["respCode"] == RESP_CODE_SUCC:
            return True, result
        else:
            return False, result

    def verify_notify_data(self, post_data):
        """
        验证银联后台交易通知
        :return: 是否验证通过, {
            "transStatus":交易状态,
            "respCode":响应码,
            "respMsg":响应信息,
            "qn":查询流水号,
            "orderNumber":商户订单号,
            "settleAmount":清算金额,
        }
        """
        is_ok, result = self._verify_signature(post_data)
        if is_ok and result["respCode"] == RESP_CODE_SUCC:
            return True, result
        else:
            return False, result

