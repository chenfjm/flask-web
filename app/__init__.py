#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from config import CONFIG


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIG['dev'])

    from sms import sms
    from ucenter import uc
    from acc import acc
    from pay import pay

    app.register_blueprint(sms, url_prefix='/sms')
    app.register_blueprint(uc, url_prefix='/uc')
    app.register_blueprint(acc, url_prefix='/acc')
    app.register_blueprint(pay, url_prefix='/pay')

    return app
