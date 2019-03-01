#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Config(object):
    SECRET_KEY = os.urandom(24)

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True


CONFIG = {
    'dev': DevConfig,
    'test': TestConfig
}
