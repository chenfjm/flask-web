#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.metasrv import MetaService
from model import UserModel


class MetaUserService(MetaService):
    def __init__(self):
        super(MetaUserService, self).__init__(UserModel)

