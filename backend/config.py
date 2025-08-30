#!/usr/bin/env python3
import os
import dotenv
from log_handler.log_handler import log as logger, Module

if os.path.isfile('.env'):
    logger.info('Found .env file, loading configs...', module=Module.SETUP)
    dotenv.load_dotenv()

DB_PATH: str = os.getenv('DB_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database/database.db'))
ML_BACKEND_URL: str = os.getenv('ML_BACKEND_URL', 'http://localhost:9090')
