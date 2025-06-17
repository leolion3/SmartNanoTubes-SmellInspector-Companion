#!/usr/bin/env python3

def get_experiments() -> str:
    return """SELECT DISTINCT TEST_ID
              FROM Data"""


def get_data_by_test_id() -> str:
    return """SELECT *
              FROM Data
              WHERE TEST_ID = ?"""


def get_substances() -> str:
    return """SELECT DISTINCT ID,
                              SUBSTANCE_NAME,
                              QUANTITY
              FROM Substance"""
