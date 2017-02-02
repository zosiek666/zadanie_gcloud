import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from zadanie.schemas import Test

NAME = 'Karol'
NOT_SPEC = 'Not specific'
ZERO_COUNT = 0
ONE_COUNT = 1
TEST = Test()


def test_serialize_return_not_specific_name_and_zero_count():
    serialized = TEST.serialize({'Name': NAME})
    assert serialized['name'] == NOT_SPEC
    assert serialized['count'] == str(ZERO_COUNT)


def test_serialize_return_proper_data():
    serialized = TEST.serialize({'name': NAME, 'count': ONE_COUNT})
    assert serialized['name'] == NAME
    assert serialized['count'] == str(ONE_COUNT)


def test_serialize_return_not_specific_if_empty_data_set():
    serialized = TEST.serialize({})
    assert serialized['name'] == NOT_SPEC
    assert serialized['count'] == str(ZERO_COUNT)
