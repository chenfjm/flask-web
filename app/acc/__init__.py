#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

acc = Blueprint('acc', __name__)

from account import views
