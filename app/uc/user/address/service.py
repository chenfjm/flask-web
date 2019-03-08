#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.ecode import ECode
from meta import MetaAddressService


class AddressService(object):
    def __init__(self):
        self.meta_srv = MetaAddressService()

    def get_detail(self, address_id):
        address = self.meta_srv.read(address_id)
        return ECode.SUCC, address

    def get_list(self):
        address_list = self.meta_srv.read_list()
