#!/usr/bin/env python3
import base64
import os.path
import threading
import time
from typing import Dict, List

import requests

import config
from database.db_handler import DatabaseHandler
from log_handler.log_handler import log as logger, Module


class MLHelper:
    """
    Sends data to the ML backend on start and gathering new data.
    """

    def _send_request_until_received(self, payload: Dict, url: str) -> None:
        while True:
            try:
                r = requests.post(url, json=payload)
                if r.status_code < 300:
                    logger.debug('Received response from ML backend:', r.text, module=Module.ML_HELPER)
                    break
            except Exception as e:
                logger.error('Error sending request to ML backend. Trace:', e, module=Module.ML_HELPER)
                time.sleep(1)
                if not self._locked:
                    self._error_count += 1
                    if self._error_count > 10:
                        self._send_initial_data()

    def _send_test_data(self, url: str) -> None:
        try:
            with open(config.DB_PATH, 'rb') as f:
                data = f.read()
            payload = {
                'data': base64.b64encode(data).decode('utf-8')
            }
            self._send_request_until_received(payload, url=url)
        except Exception as e:
            logger.error('Error reading db file. Sending no data message. Trace:', e, module=Module.ML_HELPER)
            return self._send_no_data_found(url=url)

    def _send_no_data_found(self, url: str) -> None:
        payload = {
            'data': []
        }
        self._send_request_until_received(payload, url=url)

    def _send_initial_data(self) -> None:
        """
        Sends initial data to the ML backend.
        If not data is found, send a notification with an empty data list.
        """
        self._locked = True
        try:
            url: str = config.ML_BACKEND_URL + '/initial-data'
            logger.info('Sending initial test data to ML backend...', module=Module.ML_HELPER)
            if not (os.path.exists(config.DB_PATH) and os.path.isfile(config.DB_PATH)):
                logger.warning('No data found, sending notification to ML backend...', module=Module.ML_HELPER)
                self._send_no_data_found(url=url)
                return
            self._send_test_data(url=url)
        finally:
            self._locked = False
            self._error_count = 0

    def send_new_data(self, data: List[str], substance_id: str) -> None:
        """
        Sends new data to the ML backend.
        :param data: The new data (64 string values)
        :param substance_id: The substance ID (str)
        :return:
        """
        try:
            substance, quantity = self._database.SubstanceRepository.get_substance_by_id(substance_id)
            url: str = config.ML_BACKEND_URL + '/new'
            payload = {
                'data': data,
                'substance': substance,
                'quantity': quantity
            }
            threading.Thread(target=self._send_request_until_received, args=(payload, url), daemon=True).start()
        except Exception as e:
            logger.error('Error sending new data. Trace:', e, module=Module.ML_HELPER)

    def init(self):
        logger.info('Initializing ML Helper...', module=Module.ML_HELPER)
        threading.Thread(target=self._send_initial_data, daemon=True).start()

    def __init__(self):
        self._database: DatabaseHandler = DatabaseHandler()
        self._error_count = 0
        self._locked = False


ml_helper: MLHelper = MLHelper()
