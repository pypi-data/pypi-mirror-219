import os
from time import sleep

import pytest

from dms_influx2.lib import DmsInflux2
from datetime import datetime, timedelta
from dateutil.parser import parse

from dms_influx2.utils import localize_dt

DATABASE_URL = os.environ['DATABASE_URL']
TOKEN = os.environ['TOKEN']
ORG = os.environ['ORG']
CLIENT = DmsInflux2(url=DATABASE_URL, token=TOKEN, org=ORG)

BUCKET = 'test_bucket_12345'
BUCKET_TRASH = f"{BUCKET}_trash_{datetime.now().year}"
MEASUREMENT = "test"
DEVICE_ID = "test.ch"
DESCRIPTION = "some test"
START = 0
N_SAMPLES = 10000
TEST_DATA = {
    "measurement": MEASUREMENT,
    "device_id": DEVICE_ID,
    "description": DESCRIPTION,
    "values": [(datetime.now() - timedelta(minutes=i), i) for i in range(START, N_SAMPLES)]
}


@pytest.fixture(scope='session')
def init():
    CLIENT.save_data(bucket=BUCKET, data=TEST_DATA)


def test_health():
    health = CLIENT.ping()
    assert health


def test_create_delete_bucket(init):
    bucket_name = 'abrakadabra'
    CLIENT.buckets_api().create_bucket(bucket_name=bucket_name)
    CLIENT.buckets_api().delete_bucket_by_name(bucket_name=bucket_name)
    assert CLIENT.buckets_api().bucket_exists(bucket_name) is False


def test_list_measurements(init):
    data = CLIENT.list_measurements(bucket=BUCKET)
    assert MEASUREMENT in data


def test_list_device_ids(init):
    data = CLIENT.list_device_ids(bucket=BUCKET)
    assert DEVICE_ID in data


def test_list_descriptions(init):
    data = CLIENT.list_descriptions(bucket=BUCKET, measurement=MEASUREMENT)
    assert data == [DESCRIPTION]

    data = CLIENT.list_descriptions(bucket=BUCKET)
    assert data == [DESCRIPTION]


def test_get_values_count_combined(init):
    data = CLIENT.get_values_count_combined(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID)
    assert data == N_SAMPLES


def test_get_values_count(init):
    data = CLIENT.get_values_count(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID)
    assert data[DEVICE_ID] == N_SAMPLES


def test_get_metadata(init):
    data = CLIENT.get_metadata(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID)
    assert data[0]['device_id'] == DEVICE_ID
    assert data[0]['values_count'] == N_SAMPLES
    assert data[0]['timestamp'] == str(TEST_DATA['values'][0][0])
    assert data[0]['value'] == TEST_DATA['values'][0][1]


def test_get_first_value(init):
    data = CLIENT.get_one_value(bucket=BUCKET, measurement=MEASUREMENT, last=False)
    assert data[0]['value'] == TEST_DATA['values'][-1][1]


def test_get_last_value(init):
    data = CLIENT.get_one_value(bucket=BUCKET, measurement=MEASUREMENT, last=True)
    assert data[0]['value'] == START


def test_get_last_value_sort(init):
    # Get last value with sorting (asc or desc)
    d1 = {'measurement': 'test1', 'device_id': 'test.1', 'unit': 't',
          'values': [(datetime.now() - timedelta(hours=2), 0)]}
    d2 = {'measurement': 'test1', 'device_id': 'test.2', 'unit': 't',
          'values': [(datetime.now() - timedelta(hours=0), 0)]}
    d3 = {'measurement': 'test1', 'device_id': 'test.3', 'unit': 't',
          'values': [(datetime.now() - timedelta(hours=1), 0)]}
    CLIENT.save_data(bucket=BUCKET, data=[d1, d3, d2])

    # ascending sorting
    data = CLIENT.get_one_value(bucket=BUCKET, measurement='test1', sort='asc', last=True)
    assert data[0]['device_id'] == 'test.1'
    assert data[1]['device_id'] == 'test.3'
    assert data[2]['device_id'] == 'test.2'

    # descending sorting
    data = CLIENT.get_one_value(bucket=BUCKET, measurement='test1', sort='desc', last=True)
    assert data[0]['device_id'] == 'test.2'
    assert data[1]['device_id'] == 'test.3'
    assert data[2]['device_id'] == 'test.1'


def test_get_values_from_device_id(init):
    # Descending order
    data = CLIENT.get_values_from_device_id(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID, sort='desc',
                                            time_range='all')
    assert data == list([(str(ts), val) for ts, val in TEST_DATA['values']])

    # Ascending order
    data = CLIENT.get_values_from_device_id(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID, sort='asc',
                                            time_range='all')
    assert data == [(str(ts), val) for ts, val in reversed(TEST_DATA['values'])]

    # Test different time ranges
    values = CLIENT.get_values_from_device_id(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID,
                                              time_range='all')
    assert len(values) == N_SAMPLES

    # Get values within 1 hour (60samples)
    values = CLIENT.get_values_from_device_id(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID,
                                              time_range='1h')
    assert 60 >= len(values) > 58

    # Get values within 1 day (60*24)
    values = CLIENT.get_values_from_device_id(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID,
                                              time_range='1d')
    assert 60 * 24 + 2 > len(values) > 60 * 24 - 2

    time_from = (datetime.utcnow() - timedelta(hours=10)).replace(minute=0)
    time_to = time_from + timedelta(hours=1)
    values = CLIENT.get_values_from_device_id(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID,
                                              time_from=time_from, time_to=time_to)
    assert len(values) == 60

    time_from = (datetime.utcnow() - timedelta(hours=100)).replace(minute=0)
    time_to = time_from + timedelta(hours=5)
    values = CLIENT.get_values_from_device_id(bucket=BUCKET, measurement=MEASUREMENT, device_id=DEVICE_ID,
                                              time_from=time_from, time_to=time_to)
    assert len(values) == 60 * 5


def test_range_values(init):
    dt = datetime.utcnow()
    _measurement = 'valuerange'
    _device_id = 'valuerange.1'
    _data = {
        "measurement": _measurement,
        "device_id": _device_id,
        "values": [
            (datetime(2023, 1, 22, 12, 0, 0), 0),
            (datetime(2023, 1, 22, 13, 0, 0), 1),
            (datetime(2023, 1, 22, 14, 0, 0), 2),
            (datetime(2023, 1, 22, 15, 0, 0), 3)
        ]
    }
    CLIENT.save_data(bucket=BUCKET, data=_data)

    data = CLIENT.get_values_from_device_id(bucket=BUCKET,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='greater',
                                            value=2)
    assert len(data) == 1
    assert data[0][1] == _data['values'][-1][1]

    data = CLIENT.get_values_from_device_id(bucket=BUCKET,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='lesser',
                                            value=1)
    assert len(data) == 1
    assert data[0][1] == _data['values'][0][1]

    data = CLIENT.get_values_from_device_id(bucket=BUCKET,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='range',
                                            value_within=True,
                                            value_min=1,
                                            value_max=3)
    assert len(data) == 1
    assert data[0][1] == _data['values'][2][1]

    data = CLIENT.get_values_from_device_id(bucket=BUCKET,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all',
                                            value_type='range',
                                            value_within=False,
                                            value_min=1,
                                            value_max=2)
    assert len(data) == 2
    assert data[0][1] == _data['values'][-1][1]
    assert data[1][1] == _data['values'][0][1]


def test_timezones(init):
    dt = datetime.utcnow()
    _measurement = 'timezone'
    _device_id = 'timezone.1'
    data = {
        "measurement": _measurement,
        "device_id": _device_id,
        "description": DESCRIPTION,
        "values": [(dt, 1)]
    }
    CLIENT.save_data(bucket=BUCKET, data=data)

    cl2 = DmsInflux2(url=DATABASE_URL, token=TOKEN, org=ORG)
    data = cl2.get_one_value(bucket=BUCKET, measurement=_measurement, device_id=_device_id, time_range='all')
    assert parse(data[0]['timestamp']) == dt

    cl2 = DmsInflux2(url=DATABASE_URL, token=TOKEN, org=ORG, timezone_offset=1)
    data = cl2.get_one_value(bucket=BUCKET, measurement=_measurement, device_id=_device_id, time_range='all')
    assert parse(data[0]['timestamp']) == dt + timedelta(hours=1)

    cl2 = DmsInflux2(url=DATABASE_URL, token=TOKEN, org=ORG, timezone_offset=-1)
    data = cl2.get_one_value(bucket=BUCKET, measurement=_measurement, device_id=_device_id, time_range='all')
    assert parse(data[0]['timestamp']) == dt + timedelta(hours=-1)


def test_utc_conversion(init):
    dt1 = datetime(2022, 3, 25, 12, 0, 0)
    dt2 = datetime(2022, 3, 27, 12, 0, 0)
    _measurement = 'tt'
    _device_id = 'tt.1'
    data = {
        "measurement": _measurement,
        "device_id": _device_id,
        "values": [(dt1, 1), (dt2, 2)]
    }
    CLIENT.save_data(bucket=BUCKET, data=data, utc_to_local=True)
    data = CLIENT.get_values_from_device_id(bucket=BUCKET,
                                            measurement=_measurement,
                                            device_id=_device_id,
                                            time_range='all')
    assert data[0][0] == localize_dt(dt2, to_str=True)
    assert data[-1][0] == localize_dt(dt1, to_str=True)


def test_delete_data():
    bucket = 'd_buck'
    test_data = {
        "measurement": 'deletetss',
        "device_id": 'deletetss.12',
        "values": [
            (datetime(2023, 1, 1, 12, 0, 0), 0),
            (datetime(2023, 1, 1, 12, 1, 0), 0),
            (datetime(2023, 1, 1, 12, 2, 0), 0),
            (datetime(2023, 1, 1, 12, 3, 0), 0),
            (datetime.now(), 0),
        ]
    }
    CLIENT.save_data(bucket=bucket, data=test_data)

    # Test delete time_range (from -> to)
    CLIENT.delete_api().delete_data(bucket=bucket,
                                    measurements=[test_data['measurement']],
                                    time_from=datetime(2023, 1, 1, 12, 0, 0),
                                    time_to=datetime(2023, 1, 1, 12, 2, 0))
    data = CLIENT.get_data_from_device_id(bucket=bucket,
                                          measurement=test_data['measurement'],
                                          device_id=test_data['device_id'],
                                          time_range='all')
    assert len(data['values']) == 2

    # Test delete all
    CLIENT.delete_api().delete_data(bucket=bucket,
                                    measurements=[test_data['measurement']])
    data = CLIENT.get_data_from_device_id(bucket=bucket,
                                          measurement=test_data['measurement'],
                                          device_id=test_data['device_id'],
                                          time_range='all')
    assert data == {}


def test_downsample_data():
    bucket = 'downsample_test'
    values = [(datetime.now() - timedelta(hours=i), i) for i in range(5, 100)]
    test_data = {
        "measurement": 'downsample',
        "device_id": 'downsample.12',
        "values": values

    }
    CLIENT.save_data(bucket=bucket, data=test_data)
    '''Test time_from and time_to'''
    time_from = test_data['values'][-1][0] - timedelta(seconds=1)
    time_to = test_data['values'][0][0] + timedelta(seconds=1)
    aggregate_window = '30m'
    aggregated_data = CLIENT.get_data_from_device_id(bucket=bucket,
                                                     measurement=test_data['measurement'],
                                                     device_id=test_data['device_id'],
                                                     time_from=time_from,
                                                     time_to=time_to,
                                                     aggregate_window=aggregate_window)
    # Perform a downsample and check if all data are downsampled within bucket
    CLIENT.down_sample(bucket=bucket,
                       measurement=test_data['measurement'],
                       aggregate_window=aggregate_window,
                       time_from=time_from,
                       time_to=time_to)
    data_in_downsampled_bucket = CLIENT.get_data_from_device_id(bucket=CLIENT.downsample_temp_bucket,
                                                                measurement=test_data['measurement'],
                                                                device_id=test_data['device_id'],
                                                                time_range='all')
    assert aggregated_data['values'] == data_in_downsampled_bucket['values']
    # New data in this bucket must be equal to aggregated data
    new_data = CLIENT.get_data_from_device_id(bucket=bucket,
                                              measurement=test_data['measurement'],
                                              device_id=test_data['device_id'],
                                              time_from=time_from - timedelta(seconds=1),
                                              time_to=time_to + timedelta(seconds=1))
    assert aggregated_data['values'] == new_data['values']

    '''Test2: test older_than param'''
    bucket = 'downsample_test1'
    older_than = '1d'
    aggregate_window = '4h'
    CLIENT.save_data(bucket=bucket, data=test_data)
    time_from = datetime(1970, 1, 1, 12, 0, 0)
    time_to = datetime.now() - timedelta(days=1) + timedelta(seconds=1)
    aggregated_data = CLIENT.get_data_from_device_id(bucket=bucket,
                                                     measurement=test_data['measurement'],
                                                     device_id=test_data['device_id'],
                                                     time_from=time_from,
                                                     time_to=time_to,
                                                     aggregate_window=aggregate_window)
    # Perform a downsample and check if all data are downsampled within bucket
    CLIENT.down_sample(bucket=bucket,
                       measurement=test_data['measurement'],
                       aggregate_window=aggregate_window,
                       older_than=older_than)
    data_in_downsampled_bucket = CLIENT.get_data_from_device_id(bucket=CLIENT.downsample_temp_bucket,
                                                                measurement=test_data['measurement'],
                                                                device_id=test_data['device_id'],
                                                                time_range='all')
    assert len(aggregated_data['values']) == len(data_in_downsampled_bucket['values'])
    # Old data must remain the same
    old_data = CLIENT.get_data_from_device_id(bucket=bucket,
                                              measurement=test_data['measurement'],
                                              device_id=test_data['device_id'],
                                              time_from=time_to)
    old_data_values = []
    for value in values:
        if value[0] > (time_to - timedelta(seconds=1)):
            old_data_values.append((str(value[0]), value[1]))
    assert old_data_values == old_data['values']
    new_data = CLIENT.get_data_from_device_id(bucket=bucket,
                                              measurement=test_data['measurement'],
                                              device_id=test_data['device_id'],
                                              time_from=time_from,
                                              time_to=time_to)
    assert len(aggregated_data['values']) == len(new_data['values'])
