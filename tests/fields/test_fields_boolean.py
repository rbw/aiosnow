import pytest
import marshmallow

from aiosnow.models import fields
from aiosnow.query.utils import select


def test_fields_boolean_type():
    assert isinstance(fields.Boolean(), fields.Boolean)


def test_fields_boolean_deserialize_plain_valid(mock_boolean_field):
    f_bool = mock_boolean_field("test_bool")

    assert f_bool.deserialize(True) is True
    assert f_bool.deserialize(1) is True
    assert f_bool.deserialize(False) is False
    assert f_bool.deserialize(0) is False


def test_fields_boolean_deserialize_plain_invalid(mock_boolean_field):
    with pytest.raises(marshmallow.ValidationError):
        mock_boolean_field("test_bool").deserialize(3)


def test_fields_boolean_select_falsy(mock_boolean_field):
    assert select(mock_boolean_field("test_bool").is_falsy()).sysparms == "test_bool!=true"


def test_fields_boolean_select_true(mock_boolean_field):
    assert select(mock_boolean_field("test_bool").is_true()).sysparms == "test_bool=true"
