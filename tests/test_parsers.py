"""Layer 1: XML parser helper unit tests."""

from datetime import date
from decimal import Decimal

import pytest

from gsbparse.adapters.xml.parsers import (
    parse_amount,
    parse_bool,
    parse_date,
    parse_int,
    parse_list_int,
    parse_null,
    parse_nullable_str,
    parse_optional,
    parse_str,
)
from gsbparse.domain.errors import XmlParsingError


class TestParseStr:
    def test_returns_raw_string_unchanged(self):
        dummy_value = "hello world"
        assert parse_str(dummy_value) == dummy_value

    def test_empty_string(self):
        assert parse_str("") == ""


class TestParseInt:
    def test_parses_positive_integer(self):
        dummy_raw = "42"
        assert parse_int(dummy_raw) == 42

    def test_parses_zero(self):
        assert parse_int("0") == 0

    def test_parses_negative_integer(self):
        assert parse_int("-7") == -7

    def test_raises_on_non_integer(self):
        with pytest.raises(XmlParsingError):
            parse_int("not_a_number")


class TestParseBool:
    def test_zero_is_false(self):
        assert parse_bool("0") is False

    def test_one_is_true(self):
        assert parse_bool("1") is True

    @pytest.mark.parametrize("raw", ["2", "true", "false", "yes", ""])
    def test_raises_on_unexpected_value(self, raw: str) -> None:
        with pytest.raises(XmlParsingError):
            parse_bool(raw)


class TestParseAmount:
    def test_parses_integer_amount(self):
        assert parse_amount("100") == Decimal("100")

    def test_replaces_comma_decimal_separator(self):
        dummy_raw = "42,50"
        assert parse_amount(dummy_raw) == Decimal("42.50")

    def test_parses_negative_amount(self):
        assert parse_amount("-10,00") == Decimal("-10.00")

    def test_raises_on_non_numeric(self):
        with pytest.raises(XmlParsingError):
            parse_amount("not_a_number")


class TestParseDate:
    def test_parses_us_format(self):
        dummy_raw = "12/31/2007"
        assert parse_date(dummy_raw) == date(2007, 12, 31)

    def test_parses_january(self):
        assert parse_date("01/15/2023") == date(2023, 1, 15)

    def test_raises_on_invalid_date(self):
        with pytest.raises(XmlParsingError):
            parse_date("not-a-date")


class TestParseListInt:
    def test_parses_semicolon_separated_list(self):
        dummy_raw = "1;2;3"
        assert parse_list_int(dummy_raw) == [1, 2, 3]

    def test_empty_string_returns_empty_list(self):
        assert parse_list_int("") == []

    def test_single_value(self):
        assert parse_list_int("42") == [42]

    def test_raises_on_non_integer_element(self):
        with pytest.raises(XmlParsingError):
            parse_list_int("1;x;3")


class TestParseNullableStr:
    def test_null_sentinel_returns_none(self):
        assert parse_nullable_str("(null)") is None

    def test_regular_string_returned_unchanged(self):
        dummy_value = "hello"
        assert parse_nullable_str(dummy_value) == dummy_value


class TestParseNullDecorator:
    def test_null_sentinel_short_circuits(self):
        dummy_fn = parse_null(parse_int)
        assert dummy_fn("(null)") is None

    def test_non_null_value_passed_through(self):
        dummy_fn = parse_null(parse_int)
        assert dummy_fn("7") == 7


class TestParseOptionalDecorator:
    def test_returns_none_on_xml_parsing_error(self):
        dummy_fn = parse_optional(parse_int)
        assert dummy_fn("not_an_int") is None

    def test_returns_value_on_success(self):
        dummy_fn = parse_optional(parse_int)
        assert dummy_fn("5") == 5
