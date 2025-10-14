#!/usr/bin/env python3
import os
import dotenv

if os.path.isfile('.env'):
    dotenv.load_dotenv()

DATABASE_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'persistence/database.db')
RE_TRAINING_RATE: int | str = os.getenv('RE_TRAINING_RATE')
try:
    RE_TRAINING_RATE = int(RE_TRAINING_RATE)
except Exception:
    RE_TRAINING_RATE = 100

STANDALONE_EXEC: bool = False
