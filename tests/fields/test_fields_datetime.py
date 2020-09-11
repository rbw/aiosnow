import marshmallow
import pytest

from aiosnow.models import fields
from aiosnow.query.utils import select


def test_fields_datetime_deserialize_plain_valid():
    dt = fields.DateTime()
    dt.name = "test_dt"

    result = dt.deserialize("2020-08-26 21:01:07")
    result_tz = dt.deserialize("2020-08-26T21:01:07+00:00")

    assert result.year == result_tz.year == 2020
    assert result.month == result_tz.month == 8
    assert result.day == result_tz.day == 26
    assert result.hour == result_tz.hour == 21
    assert result.minute == result_tz.minute == 1
    assert result.second == result_tz.second == 7


def test_fields_datetime_deserialize_plain_invalid():
    dt = fields.DateTime()

    with pytest.raises(marshmallow.ValidationError):
        dt.deserialize("1234-12-56 50:20:30")


def test_fields_datetime_after(mock_datetime_field):
    assert (
        select(mock_datetime_field("test_dt").after("2019-12-24 02:03:04")).sysparms
        == "test_dt>2019-12-24 02:03:04"
    )


def test_fields_datetime_as_of(mock_datetime_field):
    assert (
        select(mock_datetime_field("test_dt").as_of("2019-12-24 02:03:04")).sysparms
        == "test_dt>=2019-12-24 02:03:04"
    )


def test_fields_datetime_before(mock_datetime_field):
    assert (
        select(mock_datetime_field("test_dt").before("2019-12-24 02:03:04")).sysparms
        == "test_dt<2019-12-24 02:03:04"
    )


def test_fields_datetime_between(mock_datetime_field):
    assert (
        select(
            mock_datetime_field("test_dt").between(
                "2018-12-24 02:03:04", "2019-12-24 02:03:04"
            )
        ).sysparms
        == "test_dtBETWEEN2018-12-24 02:03:04@2019-12-24 02:03:04"
    )


def test_fields_datetime_not_on(mock_datetime_field):
    assert (
        select(mock_datetime_field("test_dt").not_on("2019-12-24 02:03:04")).sysparms
        == "test_dtNOTON2019-12-24 02:03:04"
    )


def test_fields_datetime_on(mock_datetime_field):
    assert (
        select(mock_datetime_field("test_dt").on("2019-12-24 02:03:04")).sysparms
        == "test_dtON2019-12-24 02:03:04"
    )


def test_fields_datetime_until(mock_datetime_field):
    assert (
        select(mock_datetime_field("test_dt").until("2019-12-24 02:03:04")).sysparms
        == "test_dt<=2019-12-24 02:03:04"
    )
