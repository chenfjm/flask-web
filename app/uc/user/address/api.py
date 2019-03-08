#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource
from utils.flasks import UserApi
from service import AddressService


class Address(Resource, UserApi):
    def __init__(self):
        self.address_srv = AddressService()

    def get(self, id_):
        if id_:
            code, res = self.address_srv.get_detail(id_)
        else:
            uid = self.get_args_int('uid', None)
            page = self.get_args_int('page', 1)
            psize = self.get_args_int('psize', 20)
            params = {
                'uid': uid
            }
            code, res = self.address_srv.get_list(params, page, psize)
        return self.result_json(res, code)
