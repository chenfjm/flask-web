#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

sms = Blueprint('sms', __name__)

import views
