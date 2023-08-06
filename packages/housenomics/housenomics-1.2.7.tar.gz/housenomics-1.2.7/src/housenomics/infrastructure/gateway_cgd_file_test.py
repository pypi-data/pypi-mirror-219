import pendulum
import pytest

from housenomics.infrastructure.gateway_cgd_file import RowParser


class TestRowParser:
    """
    Example of a row list:
        ['01-01-2020', '01-01-2020', 'COMPRAS C DEB FARMACI ', '15,69', '', '2.350,49', '2.350,49', 'COMPRAS ', ''] # noqa
    """

    @pytest.mark.parametrize(
        "row, expectes_error",
        [
            ([], True),
            ("", True),
            (None, True),
            (
                [
                    "MustBeAListANonEmptyList",
                ],
                False,
            ),
        ],
    )
    def test_raise_exception_when_row_is_not_valid(self, row, expectes_error):
        if not expectes_error:
            RowParser(row)
        else:
            with pytest.raises(ValueError):
                RowParser(row)

    def test_extract_value_when_debit_is_valid(self):
        row = [
            "01-01-2020",
            "",
            "COMPRAS C DEB FARMACI ",
            "2.115,69",
        ]
        row_parser = RowParser(row)

        assert row_parser.value == -2115.69  # nosec

    def test_extract_value_when_credit_is_valid(self):
        row = [
            "01-01-2020",
            "",
            "COMPRAS C DEB FARMACI ",
            "",
            "2.115,69",
        ]
        row_parser = RowParser(row)

        assert row_parser.value == 2115.69  # nosec

    def test_extract_description(self):
        row = [
            "01-01-2020",
            "",
            "COMPRAS C DEB FARMACI ",
            "",
            "2.115,69",
        ]
        row_parser = RowParser(row)

        assert row_parser.description == "COMPRAS C DEB FARMACI "  # nosec

    def test_extract_date(self):
        row = [
            "01-01-2020",
            "",
            "COMPRAS C DEB FARMACI ",
            "",
            "2.115,69",
        ]
        row_parser = RowParser(row)

        # TODO: Isolate logic to get a date object from a reversed date string
        assert row_parser.date == pendulum.parse("2020-01-01")  # nosec
