import pytest
import marshmallow

from aiosnow.query.utils import select


def test_fields_integer_deserialize_plain_valid(mock_integer_field):
    assert mock_integer_field("test_int").deserialize(123) == 123


def test_fields_integer_deserialize_plain_invalid(mock_integer_field):
    with pytest.raises(marshmallow.ValidationError):
        mock_integer_field("test_int").deserialize("asdf")


def test_fields_integer_deserialize_mapping(mock_integermap_field):
    loaded = mock_integermap_field("test_int").deserialize((3, "3 - High"))

    assert loaded.key == 3
    assert loaded.value == "3 - High"


def test_fields_integer_query_between(mock_integer_field):
    assert select(mock_integer_field("test_int").between(1, 3)).sysparms == "test_intBETWEEN1@3"


def test_fields_integer_query_equals(mock_integer_field):
    assert select(mock_integer_field("test_int").equals(0)).sysparms == "test_int=0"


def test_fields_integer_greater_or_equals(mock_integer_field):
    assert select(mock_integer_field("test_int").greater_or_equals(0)).sysparms == "test_int>=0"


def test_fields_integer_greater_than(mock_integer_field):
    assert select(mock_integer_field("test_int").greater_than(2)).sysparms == "test_int>2"


def test_fields_integer_less_or_equals(mock_integer_field):
    assert select(mock_integer_field("test_int").less_or_equals(2)).sysparms == "test_int<=2"


def test_fields_integer_less_than(mock_integer_field):
    assert select(mock_integer_field("test_int").less_than(2)).sysparms == "test_int<2"


def test_fields_integer_not_equals(mock_integer_field):
    assert select(mock_integer_field("test_int").not_equals(2)).sysparms == "test_int!=2"
