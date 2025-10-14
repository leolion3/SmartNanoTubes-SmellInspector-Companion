#!/usr/bin/env python3
import base64
import os.path
import sqlite3
import traceback
import uuid
import config
from typing import Dict, List, Any

import config
from logging_framework.log_handler import log as logger, Module
from ml_adapters import data_relabeller
from persistence.queries import data_queries


class DatabaseHandler:
    DATA_LABELS: List[str] = [f'DATA_{i}' for i in range(64)]

    @staticmethod
    def _delete_if_exists() -> None:
        if os.path.exists(config.DATABASE_FILE_PATH) and config.STANDALONE_EXEC:
            os.remove(config.DATABASE_FILE_PATH)
            logger.info('Deleted cached database file.', module=Module.DB)

    def _init_db(self) -> sqlite3.Connection:
        self._delete_if_exists()
        conn = sqlite3.connect(config.DATABASE_FILE_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        q: str = data_queries.create_data_table_query()
        conn.execute(q)
        conn.commit()
        return conn

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

    def _get_data(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        res = []
        for row in results:
            try:
                _row = dict(row)
                _data = {
                    'label': _row['label'],
                    'data': self._get_sensor_data_from_row(_row)
                }
                if _data['label'].strip() != 'air':
                    _data['quantity'] = _row['quantity'].replace('mu', 'μl')
                res.append(_data)
            except Exception as e:
                logger.error('Error formatting db row. Trace:', e, module=Module.DB)
                logger.error(traceback.format_exc(), module=Module.DB)
        return res

    def get_labelled_data(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        q: str = data_queries.get_data_query()
        results: List[Dict[str, Any]] = cursor.execute(q).fetchall()
        return self._get_data(results)

    def add_data(self, data: List[str], label: str, quantity: str) -> None:
        try:
            q: str = data_queries.persist_data_query()
            self.conn.execute(q, (*data, label, quantity))
            self.conn.commit()
        except Exception as e:
            logger.error('Error persisting data. Trace:', e, module=Module.DB)
            logger.error(traceback.format_exc(), module=Module.DB)

    @staticmethod
    def _fetch_experiments(conn: sqlite3.Connection):
        cursor = conn.cursor()
        results = cursor.execute(data_queries.get_experiments()).fetchall()
        return [dict(result)['TEST_ID'] for result in results]

    @staticmethod
    def _fetch_substances(conn: sqlite3.Connection):
        cursor = conn.cursor()
        results: List[Dict[str, Any]] = cursor.execute(data_queries.get_substances()).fetchall()
        results = [dict(result) for result in results]
        return {
            str(result['ID']): {
                'name': result['SUBSTANCE_NAME'],
                'quantity': result['QUANTITY']
            }
            for result in results
        }

    @staticmethod
    def _get_quantity_for_substance(substances, result):
        try:
            return substances[result['SUBSTANCE_ID']][1]
        except:
            logger.error('Found no quantity, using default: 0.')
            return ''

    def _get_data_for_experiment(
            self,
            conn: sqlite3.Connection,
            experiment_name: str,
            substances: Dict[str, Dict[str, str]],
            re_label_using_avg_humidity: bool
    ) -> List[Dict[str, Any]]:
        """
        Get all data for a given experiment name.
        :param experiment_name: the name of the experiment.
        :return: data for the given experiment.
        """
        q: str = data_queries.get_data_by_test_id()
        cursor: sqlite3.Cursor = conn.cursor()
        results: List[Dict[str, Any]] = cursor.execute(q, [experiment_name]).fetchall()
        results = [dict(result) for result in results]
        logger.debug('substances:', dict(results[0]))
        data: List[Dict[str, Any]] = [{
            'label': substances[result['SUBSTANCE_ID']]['name'].lower(),
            'quantity': substances[result['SUBSTANCE_ID']].get('quantity', '').lower(),
            'data': self._get_sensor_data_from_row(dict(result)),
            'humidity': result['HUMIDITY']
        } for result in results]
        if re_label_using_avg_humidity:
            logger.info('Re-labeling data with average humidity.', module=Module.DB)
            data_relabeller.re_label_data(data)
        for dp in data:
            dp.pop('humidity', None)
        return data

    def _parse_data(self, filepath: str, re_label_using_avg_humidity: bool = True) -> None:
        try:
            conn = sqlite3.connect(filepath, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            experiments = self._fetch_experiments(conn)
            substances = self._fetch_substances(conn)
            all_data = []
            for experiment in experiments:
                logger.debug('Fetching data for experiment', experiment, module=Module.DB)
                all_data.extend(self._get_data_for_experiment(
                    conn=conn,
                    experiment_name=experiment,
                    substances=substances,
                    re_label_using_avg_humidity=re_label_using_avg_humidity
                ))
            logger.info('Persisting data...', module=Module.DB)
            for dp in all_data:
                self.add_data(
                    data=[str(i) for i in dp['data']],
                    label=dp['label'],
                    quantity=dp['quantity']
                )
        except Exception as e:
            logger.error('Error parsing data. Trace:', e, module=Module.DB)
            logger.error(traceback.format_exc(), module=Module.DB)

    def persist_from_db_data(self, data: str) -> None:
        try:
            logger.info('Resetting database...', module=Module.DB)
            self.conn = self._init_db()
            logger.info('Attempting to load data from db file...', module=Module.DB)
            temp_filename: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), uuid.uuid4().hex + '.db')
            data = base64.b64decode(data)
            with open(temp_filename, 'wb') as f:
                f.write(data)
            self._parse_data(temp_filename)
            os.remove(temp_filename)
            logger.info('Loaded data from db file.', module=Module.DB)
        except Exception as e:
            logger.error('Error persisting data from companion software. Trace:', e, module=Module.DB)

    def __init__(self):
        logger.info('Starting Database Handler...', module=Module.DB)
        self.conn: sqlite3.Connection = self._init_db()
        logger.info('Database Handler initialized.', module=Module.DB)


database_handler: DatabaseHandler = DatabaseHandler()
