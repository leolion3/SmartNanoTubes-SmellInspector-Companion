#!/usr/bin/env python3
import csv
import os
from typing import Tuple, List

from log_handler.log_handler import Module, log as logger


class CSVHandler:
    """
    Handles csv import/export.
    """
    CSV_DELIMITER = os.getenv('CSV_DELIMITER') or ';'
    CSV_ESCAPE_CHARACTER = os.getenv('CSV_ESCAPE_CHARACTER') or '"'

    @staticmethod
    def __write_header(writer, headers: [str]) -> None:
        """
        Write the csv headers to the export file.
        :param headers: the csv headers as a list of strings.
        :return:
        """
        logger.info('Writing CSV headers...', module=Module.CSV)
        logger.debug('Headers:', headers, module=Module.CSV)
        writer.writerow(headers)

    @staticmethod
    def __write_content(writer, content: [[str]]) -> None:
        """
        Write the csv content.
        :param content: the csv content.
        :return:
        """
        logger.info('Writing CSV content to file...', module=Module.CSV)
        filtered = []
        for line in content:
            filtered_line = [str(item) if item is not None else '' for item in line]
            filtered.append(filtered_line)
            logger.debug('Writing row:', filtered_line, module=Module.CSV)
        writer.writerows(filtered)

    def export(self, headers: List[str], data: List[List[str]], filename: str) -> str:
        """
        Public interface for exporting csv data.
        :return:
        """
        logger.info('Starting export...', module=Module.CSV)
        with open(filename, 'w+') as f:
            writer = csv.writer(
                f,
                delimiter=self.CSV_DELIMITER,
                quotechar=self.CSV_ESCAPE_CHARACTER,
                escapechar='\\',
                lineterminator='\n'
            )
            self.__write_header(writer=writer, headers=headers)
            self.__write_content(writer=writer, content=data)
            f.flush()
        logger.info(f'Data exported to {filename}.', module=Module.CSV)
        return filename

    def __read_csv_values(self, file_ptr) -> List[List[str]]:
        """
        Read the csv data into a 2d string list.
        :param file_ptr: pointer for reading csv file.
        :return: the read values.
        """
        logger.debug(f'Setting up parser with delimiter \"{self.CSV_DELIMITER}\" '
                     + f'and escape char \"{self.CSV_ESCAPE_CHARACTER}\"...', module=Module.CSV)
        csv_reader = csv.reader(file_ptr, delimiter=self.CSV_DELIMITER, quotechar=self.CSV_ESCAPE_CHARACTER)
        file_ptr.seek(0)
        next(csv_reader, None)
        values = [row for row in csv_reader]
        return values

    def __read_csv_header(self, file_ptr) -> List[str]:
        """
        Read the csv headers.
        :param file_ptr: pointer for reading csv file.
        :return: the csv headers as a list.
        """
        csv_reader = csv.reader(file_ptr, delimiter=self.CSV_DELIMITER)
        headers = next(csv_reader, None)
        logger.debug(f'Reading Headers: {headers}, length: {len(headers)}', module=Module.CSV)
        return headers

    def import_csv(self, filepath: str) -> Tuple[List[str], List[List[str]]]:
        """
        Import csv data from file to db in testmode.
        :return:
        """
        with open(filepath, 'r') as f:
            logger.debug('Reading CSV headers...', module=Module.CSV)
            headers = self.__read_csv_header(file_ptr=f)
            logger.debug('Reading CSV content...', module=Module.CSV)
            content = self.__read_csv_values(file_ptr=f)
            return headers, content
