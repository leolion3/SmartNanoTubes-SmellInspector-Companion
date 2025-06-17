#!/usr/bin/env python3
import os
import sqlite3
from typing import Dict, Any, List

from logging_framework.log_handler import Module, log
from persistence.queries import data_queries


class DatabaseHandler:
    """
    Handles database operations.
    """
    DATA_LABELS: List[str] = [f'DATA_{i}' for i in range(64)]

    def get_substances(self) -> Dict[str, str]:
        """
        Get the available substances for the given database.
        :return: a list of available substances.
        """
        q: str = data_queries.get_substances()
        cursor: sqlite3.Cursor = self._conn.cursor()
        results: List[Dict[str, Any]] = cursor.execute(q).fetchall()
        return {
            str(dict(result)['ID']): dict(result)['SUBSTANCE_NAME']
            for result in results
        }

    def get_experiment_list(self) -> List[str]:
        """
        Get a list of recorded experiments for the given database.
        :return: a list of experiment names.
        :return:
        """
        q: str = data_queries.get_experiments()
        cursor: sqlite3.Cursor = self._conn.cursor()
        results: List[Dict[str, Any]] = cursor.execute(q).fetchall()
        return [dict(result)['TEST_ID'] for result in results]

    def _get_sensor_data_from_row(self, row: Dict[str, Any]) -> List[Any]:
        """
        Extracts the DATA_O-DATA_63 values from the given database row.
        :param row: the database row.
        :return: the sensor data ordered from 0 to 63.
        """
        data: List[Any] = []
        for label in self.DATA_LABELS:
            data.append(float(row[label]))
        return data

    def get_labelled_data(self, experiment_name: str) -> List[Dict[str, Any]]:
        """
        Get all data for a given experiment name.
        :param experiment_name: the name of the experiment.
        :return: data for the given experiment.
        """
        substances: Dict[str, str] = self.get_substances()
        q: str = data_queries.get_data_by_test_id()
        cursor: sqlite3.Cursor = self._conn.cursor()
        results: List[Dict[str, Any]] = cursor.execute(q, [experiment_name]).fetchall()
        return [{
            'label': substances[dict(result)['SUBSTANCE_ID']],
            'data': self._get_sensor_data_from_row(dict(result))
        } for result in results]

    def __init__(self, db_path: str) -> None:
        """
        Default constructor.
        :param db_path: path to the database file.
        """
        try:
            log.info(f'Connecting to database {db_path}...', module=Module.DB)
            if not os.path.isfile(db_path):
                raise IOError(f'File {db_path} does not exist.')
            self._conn: sqlite3.Connection = sqlite3.connect(db_path)
            self._conn.row_factory = sqlite3.Row
            log.info('Connection established.', module=Module.DB)
        except Exception as e:
            log.error('Error starting DB Handler. Trace:', e, module=Module.DB)
            raise
