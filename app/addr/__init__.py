#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

addr = Blueprint('address', __name__)

from address import views
