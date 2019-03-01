#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from config import CONFIG


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIG['dev'])

    from ucenter import uc as ucenter_blueprint
    app.register_blueprint(ucenter_blueprint, url_prefix='/uc')

    from acc import acc as acc_blueprint
    app.register_blueprint(acc_blueprint, url_prefix='/acc')

    from pay import pay as pay_blueprint
    app.register_blueprint(pay_blueprint, url_prefix='/pay')

    return app
