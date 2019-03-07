#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

sms_bp = Blueprint('sms', __name__)

import views
