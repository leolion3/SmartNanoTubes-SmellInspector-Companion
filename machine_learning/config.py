#!/usr/bin/env python3
import os
import dotenv

from typing import Optional
from logging_framework.log_handler import log, Module

from ml_adapters.abstract_ml_adapter import SampleStrategy

if os.path.isfile('.env'):
    dotenv.load_dotenv()

DATABASE_FILE_PATH: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'persistence/database.db')
RE_TRAINING_RATE: int | str = os.getenv('RE_TRAINING_RATE')
ENABLE_QUANTITIES: bool | str = os.getenv('ENABLE_QUANTITIES', False)
BALANCE_DATASET: bool | str = os.getenv('BALANCE_DATASET', True)
BALANCE_STRATEGY: str | SampleStrategy = os.getenv('BALANCE_STRATEGY', 'UNDERSAMPLE')
ENABLE_HUMIDITY: bool | str = os.getenv('ENABLE_HUMIDITY', True)
COMPUTE_AVERAGES: bool | str = os.getenv('COMPUTE_AVERAGES', True)
HUMIDITY_ONLY: bool | str = os.getenv('HUMIDITY_ONLY', False)  # Experimental
try:
    RE_TRAINING_RATE = int(RE_TRAINING_RATE)
except Exception:
    RE_TRAINING_RATE = 100


def parse_boolean(value: Optional[str] | bool) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or not len(value.strip()):
        return False
    return 'true' in value.lower()


def parse_sample_strategy(value: str) -> SampleStrategy:
    if value is None:
        return SampleStrategy.OVERSAMPLE
    if 'under' in value.lower():
        return SampleStrategy.UNDERSAMPLE
    return SampleStrategy.OVERSAMPLE


ENABLE_QUANTITIES = parse_boolean(ENABLE_QUANTITIES)
BALANCE_DATASET = parse_boolean(BALANCE_DATASET)
ENABLE_HUMIDITY = parse_boolean(ENABLE_HUMIDITY)
COMPUTE_AVERAGES = parse_boolean(COMPUTE_AVERAGES)
HUMIDITY_ONLY = parse_boolean(HUMIDITY_ONLY)
BALANCE_STRATEGY = parse_sample_strategy(BALANCE_STRATEGY)

log.info(
    'Running ML Adapter with configs:',
    '\nRe-Training Rate:', RE_TRAINING_RATE,
    '\nQuantities enabled:', ENABLE_QUANTITIES,
    '\nBalancing enabled:', BALANCE_DATASET,
    '\nBalance strategy:', BALANCE_STRATEGY,
    '\nHumidity enabled:', ENABLE_HUMIDITY,
    '\nCompute Averages:', COMPUTE_AVERAGES,
    '\nHumidity only (Experimental):', HUMIDITY_ONLY,
    module=Module.SETUP
)

STANDALONE_EXEC: bool = False
