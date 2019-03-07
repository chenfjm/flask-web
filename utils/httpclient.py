#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
proxy高可用Http Client
"""
import time
import json
import random
import socket
import urllib
import urllib2
import urlparse
import logging
import mimetypes
from .util import force_utf8


class HttpClient(object):
    """
    高可用HttpClient
    """
    HTTP_GET = "GET"
    HTTP_POST = "POST"
    HTTP_UPLOAD = "UPLOAD"  # 注意这里不是标准的HTTP METHOD, 最终还是发送HTTP POST

    def __init__(self, proxy_list=None, timeout=5):
        """
        初始化
        :param list proxy_list: 代理列表
        :param int timeout: 超时时间
        """
        self._proxy_map = {}

        # 代理字典
        proxy_list = proxy_list or []
        for i in proxy_list:
            self._proxy_map[i] = {
                "fail_count": 0,
                "fail_time": 0
            }

        # 代理的失败阈值, 三次
        self.fail_threshold = 3

        # 代理的失败阈值, 秒
        self.retry_timeout = 600

        # HTTP的超时时间
        self.timeout = timeout

    def choose_proxy(self):
        """
        选取当前可用的代理
        """
        now = int(time.time())

        # 遍历当前代理
        for i in self._proxy_map:
            stats = self._proxy_map[i]

            # 小于失败阈值 或 过了重试时间
            if stats["fail_count"] <= self.fail_threshold:
                return i
            if now > stats["fail_time"] + self.retry_timeout:
                return i

        # 如果都没有可用的, 随机选取一个
        if not self._proxy_map:
            return None
        index = int(random.random() * 1000) % len(self._proxy_map)
        return self._proxy_map.keys()[index]

    def set_proxy_succ(self, proxy):
        """
        设置代理可用
        """
        if proxy:
            self._proxy_map[proxy] = {"fail_count": 0, "fail_time": 0}

    def set_proxy_fail(self, proxy):
        """
        设置代理不可用
        """
        if proxy:
            stats = self._proxy_map[proxy]
            stats["fail_count"] += 1
            stats["fail_time"] = int(time.time())
            logging.warn("set_proxy_fail proxy: %s", proxy)

    @staticmethod
    def encode_params(**kargs):
        """
        编码URL参数
        :param dict kargs: 参数信息--字典
        :return: url编码后的参数
        """
        args = []
        for k, v in kargs.iteritems():
            if v is None:
                continue
            qv = v.encode("utf-8") if isinstance(v, unicode) else str(v)
            args.append("%s=%s" % (k, urllib.quote(qv)))
        return "&".join(args)

    @staticmethod
    def encode_multipart(**kargs):
        """
        根据随机boundary创建 multipart/form-data body
        :param dict kargs: 参数信息--字典
        :return: http body
        """
        boundary = "----------%s" % hex(int(time.time() * 1000))
        data = []
        for k, v in kargs.iteritems():
            if v is None:
                continue
            if isinstance(v, list):   # 文件对象, v: [[filename, file_obj],[filename2, file_obj2]]
                for item in v:
                    data.append("--%s" % boundary)
                    file_name, file_obj = item[0], item[1]
                    if isinstance(file_name, unicode):
                        file_name = file_name.encode("utf-8")
                    mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
                    content = file_obj.read() if hasattr(file_obj, "read") else file_obj
                    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (k, file_name))
                    data.append("Content-Length: %d" % len(content))
                    data.append("Content-Type: %s\r\n" % mime_type)
                    data.append(content)
            else:
                data.append("--%s" % boundary)
                data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
                data.append(v.encode("utf-8") if isinstance(v, unicode) else str(v))
        data.append("--%s--\r\n" % boundary)
        return "\r\n".join(data), boundary

    def http_get(self, url, resp_format="json", headers=None, **kargs):
        """
        发起GET请求
        :param str url: 请求URL
        :param str resp_format: 返回格式
        :param dict headers: Http Header
        :param dict kargs: 参数信息--字典
        :return: 响应内容
        """
        return self._http_call(url, self.HTTP_GET, resp_format, headers,
                               None, **kargs)

    def http_post(self, url, resp_format="json", headers=None, body=None,
                  **kargs):
        """
        发起POST请求
        :param str url: 请求URL
        :param str resp_format: 返回格式
        :param dict kargs: 参数信息--字典
        :return: 响应内容
        """
        return self._http_call(url, self.HTTP_POST, resp_format, headers,
                               body, **kargs)

    def http_upload(self, url, resp_format="json", headers=None, **kargs):
        """
        发起UPLOAD请求
        :param str url: 请求URL
        :param str resp_format: 返回格式
        :param dict kargs: 参数信息--字典
        :return: 响应内容
        """
        return self._http_call(url, self.HTTP_UPLOAD, resp_format, headers,
                               None, **kargs)

    def _http_call(self, url, http_method, resp_format="json", headers=None,
                   body=None, **kargs):
        """
        发送HTTP请求
        """
        # 根据不同http_method生成参数
        params, boundary = None, None
        if http_method == self.HTTP_UPLOAD:
            params, boundary = self.encode_multipart(**kargs)
        else:
            params = self.encode_params(**kargs)

        # URL body
        if http_method == self.HTTP_GET:
            http_url, http_body = "%s?%s" % (url, params) if params else url, None
        else:
            http_url, http_body = url, params

        # 当http_method为POST, 并且body不为空
        if http_method == self.HTTP_POST and body:
            http_body = body

        # 构造请求
        req = urllib2.Request(http_url, data=http_body)
        if headers:
            for name in headers:
                req.add_header(name, headers[name])
        if boundary:
            req.add_header("Content-Type", "multipart/form-data; boundary=%s" % boundary)

        # 是否启用代理
        proxy, res = self.choose_proxy(), None
        logging.info("choose proxy: %s", proxy)
        try:
            if proxy:
                proxy_support = urllib2.ProxyHandler({
                    "http": proxy,
                    "https": proxy
                })
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler,
                                              urllib2.HTTPSHandler)
                resp = opener.open(req, timeout=self.timeout)
            else:
                resp = urllib2.urlopen(req, timeout=self.timeout)
            res = resp.read()
            resp.close()
        except (urllib2.URLError, socket.error), e:
            self.set_proxy_fail(proxy)
            raise e
        else:
            self.set_proxy_succ(proxy)

        # 解析内容
        if resp_format == "json" or resp_format == "jsonp":
            if resp_format == "jsonp":
                res = res[res.index("{"):res.rindex("}") + 1]
            res = json.loads(res, object_hook=self._obj_hook)
        elif resp_format == "uriqs":
            res = self._parse_uriqs(res)
        return force_utf8(res)

    @staticmethod
    def _obj_hook(pairs):
        """
        转换Json到Python对象
        """
        o = JsonObject()
        for k, v in pairs.iteritems():
            o[force_utf8(k)] = force_utf8(v)
        return o

    @staticmethod
    def _parse_uriqs(content):
        """
        convert uri query sting to python object.
        转换URI查询串到Python对象
        """
        o = JsonObject()
        pairs = urlparse.parse_qs(content)
        for k, v in pairs.iteritems():
            o[force_utf8(k)] = v[0]
        return o


class JsonObject(dict):
    """
    通用Json对象, 能绑定任何字段, 行为类似dict
    """
    def __getattr__(self, attr):
        """
        读取属性
        """
        return self[attr]

    def __setattr__(self, attr, value):
        """
        设置属性
        """
        self[attr] = value

