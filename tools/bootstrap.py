#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from flask_sqlalchemy import SQLAlchemy
from flask import current_app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-cmd', type=str, default='create_tables',
                        help='create_tables, drop_tables')

    args = parser.parse_args()
    if args.cmd == 'create_tables':
        db = SQLAlchemy(current_app)
        db.create_all()
    if args.cmd == 'drop_tables':
        db = SQLAlchemy(current_app)
        db.drop_all()

