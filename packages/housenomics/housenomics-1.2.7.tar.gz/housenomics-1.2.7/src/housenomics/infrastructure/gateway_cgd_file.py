import csv
import pathlib

import pendulum

from housenomics.transaction import Transaction


class RowParser:
    """
    Example of a row list:
        ['01-01-2020', '01-01-2020', 'COMPRAS C DEB FARMACI ', '15,69', '', '2.350,49', '2.350,49', 'COMPRAS ', ''] # noqa
    """

    def __init__(self, row: list):
        if not row:
            raise ValueError("Row cannot be empty")

        self.row = row

    @property
    def value(self) -> float:
        """
        Get the value of the transaction.
        """

        debit_row_index = 3
        credit_row_index = 4

        value_index = debit_row_index
        if not self.row[debit_row_index]:
            value_index = credit_row_index

        parsed_value = self.row[value_index].replace(".", "").replace(",", ".")

        if value_index == credit_row_index:
            return float(parsed_value)

        return float(parsed_value) * -1

    @property
    def description(self) -> str:
        """
        Get the description of the transaction.
        """

        return self.row[2]

    @property
    def date(self):
        """
        Get the date of the transaction.
        """

        raw_date = self.row[0]
        splited_date = raw_date.split("-")
        splited_date.reverse()
        joined_date = "-".join(splited_date)
        return pendulum.parse(joined_date)


class GatewayCGDFile:
    """
    Example of a file:
        Consultar saldos e movimentos � ordem - 09-08-2022

        Conta ;1234567890 - EUR - Conta Caderneta
        Data de in�cio ;01-01-2020
        Data de fim ;09-08-2022

        Data mov. ;Data valor ;Descri��o ;D�bito ;Cr�dito ;Saldo contabil�stico ;Saldo dispon�vel ;Categoria ; # noqa
        01-01-2020;01-01-2020;COMPRAS C DEB FARMACI ;15,69;;2.350,49;2.350,49;COMPRAS ;
        09-08-2022;09-08-2022;TRF  ;;45,00;2.133,88;2.133,88;Diversos ;
        ; ; ; ;Saldo contabil�stico ;2.094,08 EUR ; ; ;
    """

    def __init__(self, csv_file_path: pathlib.Path):
        self.csv_file_path = csv_file_path
        self.read_obj = None

    def __iter__(self):
        self.read_obj = open(self.csv_file_path, "r", encoding="ISO-8859-1")
        self.csv_reader = csv.reader(self.read_obj, delimiter=";")

        return _Converter(self.csv_reader)

    def __del__(self):
        if self.read_obj is not None:
            self.read_obj.close()


class _Converter:
    def __init__(self, csv_reader):
        self._reader = csv_reader

        # Ignore the headers of the file, 7 lines
        for _ in range(7):
            next(self._reader)

    def __next__(self):
        row = next(self._reader)

        # Ignore last lines of the file
        if "('" in row[0]:
            raise StopIteration

        row_parser = RowParser(row)

        t = Transaction(
            description=row_parser.description,
            date_of_movement=row_parser.date,
            value=row_parser.value,
            origin="CGD",
        )

        return t
