#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.metasrv import MetaService
from model import AddressModel


class MetaAddressService(MetaService):
    def __init__(self):
        super(MetaAddressService, self).__init__(AddressModel)
