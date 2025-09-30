#!/usr/bin/env python3


def create_data_table_query() -> str:
    return ("CREATE TABLE IF NOT EXISTS data ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT, "
            f"{', '.join([f'DATA_{i} TEXT' for i in range(64)])}, "
            "label TEXT NOT NULL,"
            "quantity TEXT);")


def persist_data_query() -> str:
    return f'INSERT INTO data values (NULL, {", ".join(["?" for _ in range(64)])}, ?, ?)'


def get_data_query() -> str:
    return 'SELECT * FROM data'


def get_experiments() -> str:
    return """SELECT DISTINCT TEST_ID
              FROM Data"""


def get_data_by_test_id() -> str:
    return """SELECT *
              FROM Data
              WHERE TEST_ID = ?"""


def get_substances() -> str:
    return """SELECT ID, SUBSTANCE_NAME, QUANTITY
              FROM Substance"""
