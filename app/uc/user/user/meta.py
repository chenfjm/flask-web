#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.metasrv import MetaService
from model import UserModel


class MetaUserService(MetaService):
    def __init__(self):
        super(MetaUserService, self).__init__(UserModel)

    def read_by_phone(self, phone):
        user = self._model.query.filter_by(phone=phone).first()
        return user
