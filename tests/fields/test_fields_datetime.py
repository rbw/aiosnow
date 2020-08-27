import pytest

from aiosnow.exceptions import DeserializationError
from aiosnow.models.common.schema import BaseSchema, fields
from aiosnow.query.utils import select


def test_fields_datetime_type():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    schema = TestSchema()
    assert isinstance(schema.test_dt, fields.DateTime)


def test_fields_datetime_deserialize_plain_valid():
    class TestSchema(BaseSchema):
        test_dt1 = fields.DateTime()
        test_dt2 = fields.DateTime()

    schema = TestSchema()
    data = schema.load(
        {"test_dt1": "2020-08-26 21:01:07", "test_dt2": "2020-08-26T21:01:07+00:00"}
    )

    assert data["test_dt1"].year == data["test_dt2"].year == 2020
    assert data["test_dt1"].month == data["test_dt2"].month == 8
    assert data["test_dt1"].day == data["test_dt2"].day == 26
    assert data["test_dt1"].hour == data["test_dt2"].hour == 21
    assert data["test_dt1"].minute == data["test_dt2"].minute == 1
    assert data["test_dt1"].second == data["test_dt2"].second == 7


def test_fields_datetime_deserialize_plain_invalid():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    schema = TestSchema()

    with pytest.raises(DeserializationError):
        schema.load({"test_dt": "1234-12-56 50:20:30"})


def test_fields_datetime_after():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    assert select(TestSchema.test_dt.after("2019-12-24 02:03:04")).sysparms == "test_dt>2019-12-24 02:03:04"


def test_fields_datetime_as_of():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    assert select(TestSchema.test_dt.as_of("2019-12-24 02:03:04")).sysparms == "test_dt>=2019-12-24 02:03:04"


def test_fields_datetime_before():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    assert select(TestSchema.test_dt.before("2019-12-24 02:03:04")).sysparms == "test_dt<2019-12-24 02:03:04"


def test_fields_datetime_between():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    assert select(TestSchema.test_dt.between("2018-12-24 02:03:04", "2019-12-24 02:03:04")).sysparms == "test_dtBETWEEN2018-12-24 02:03:04@2019-12-24 02:03:04"


def test_fields_datetime_not_on():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    assert select(TestSchema.test_dt.not_on("2019-12-24 02:03:04")).sysparms == "test_dtNOTON2019-12-24 02:03:04"


def test_fields_datetime_on():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    assert select(TestSchema.test_dt.on("2019-12-24 02:03:04")).sysparms == "test_dtON2019-12-24 02:03:04"


def test_fields_datetime_until():
    class TestSchema(BaseSchema):
        test_dt = fields.DateTime()

    assert select(TestSchema.test_dt.until("2019-12-24 02:03:04")).sysparms == "test_dt<=2019-12-24 02:03:04"
