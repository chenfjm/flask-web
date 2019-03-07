#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.default')
    app.config.from_envvar('APP_CONFIG_FILE')

    from sms import sms_bp
    from uc import uc
    from acc import acc
    from pay import pay
    from addr import addr

    app.register_blueprint(sms_bp, url_prefix='/sms')
    app.register_blueprint(uc, url_prefix='/uc')
    app.register_blueprint(acc, url_prefix='/acc')
    app.register_blueprint(pay, url_prefix='/pay')
    app.register_blueprint(addr, url_prefix='/address')

    return app
