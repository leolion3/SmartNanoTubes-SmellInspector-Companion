#!/usr/bin/env python3
import os

from logging_framework.log_handler import Logger, log

DATA_DIR: str = 'data'
DATABASE_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_DIR, 'database.db')
