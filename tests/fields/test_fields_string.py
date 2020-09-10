import pytest
import marshmallow

from aiosnow.query.utils import select


def test_fields_string_deserialize_plain_valid(mock_string_field):
    assert mock_string_field("test_str").deserialize("test123") == "test123"


def test_fields_string_deserialize_plain_invalid(mock_string_field):
    with pytest.raises(marshmallow.ValidationError):
        mock_string_field("test_str").deserialize(1)


def test_fields_string_deserialize_mapping(mock_stringmap_field):
    loaded = mock_stringmap_field("test_str").deserialize(("a83820b58f723300e7e16c7827bdedd2", "Hello"))

    assert loaded.key == "a83820b58f723300e7e16c7827bdedd2"
    assert loaded.value == "Hello"


def test_fields_string_query_between(mock_stringmap_field):
    assert (
        select(mock_stringmap_field("test_str").between("q", "t")).sysparms == "test_strBETWEENq@t"
    )


def test_fields_string_query_ends_with(mock_stringmap_field):
    assert (
        select(mock_stringmap_field("test_str").ends_with("outage")).sysparms
        == "test_strENDSWITHoutage"
    )


def test_fields_string_query_equals(mock_stringmap_field):
    assert select(mock_stringmap_field("test_str") == "test").sysparms == "test_str=test"
    assert select(mock_stringmap_field("test_str").equals("test")).sysparms == "test_str=test"


def test_fields_string_query_greater_or_equals(mock_stringmap_field):
    assert select(mock_stringmap_field("test_str").greater_or_equals("s")).sysparms == "test_str>=s"


def test_fields_string_query_less_or_equals(mock_stringmap_field):
    assert select(mock_stringmap_field("test_str").less_or_equals("s")).sysparms == "test_str<=s"


def test_fields_string_query_not_contains(mock_stringmap_field):
    assert select(mock_stringmap_field("test_str").not_contains("SAP")).sysparms == "test_str!*SAP"


def test_fields_string_query_not_equals(mock_stringmap_field):
    assert (
        select(
            mock_stringmap_field("test_str").not_equals("Network storage is unavailable")
        ).sysparms
        == "test_str!=Network storage is unavailable"
    )
