import os

from dms_influx2.lib import DmsInflux2
from datetime import datetime, timedelta
from dotenv import dotenv_values

DATABASE_URL = os.environ['DATABASE_URL']
TOKEN = os.environ['TOKEN']
ORG = os.environ['ORG']
CLIENT = DmsInflux2(url=DATABASE_URL, token=TOKEN, org=ORG)

BUCKET = 'test_bucket_12345'
START = 0
N_SAMPLES = 5
TEST_DATA_1 = {
    "measurement": 'testcopy',
    "device_id": 'testcopy.1',
    "values": [(datetime.now().replace(microsecond=0) - timedelta(minutes=i), i)
               for i in range(START, N_SAMPLES)]
}

TEST_DATA_2 = {
    "measurement": 'testcopy2',
    "device_id": 'testcopy.2',
    "values": [(datetime.now().replace(microsecond=0) - timedelta(minutes=i), i)
               for i in range(N_SAMPLES + 1, N_SAMPLES + N_SAMPLES)]
}


def test_copy_values():
    if CLIENT.buckets_api().bucket_exists(bucket_name=BUCKET):
        CLIENT.buckets_api().delete_bucket_by_name(bucket_name=BUCKET)
    CLIENT.buckets_api().create_bucket(bucket_name=BUCKET)

    CLIENT.delete_api().delete_data(bucket=BUCKET, measurements=['testcopy', 'testcopy2'])
    CLIENT.save_data(bucket=BUCKET, data=TEST_DATA_1)
    CLIENT.save_data(bucket=BUCKET, data=TEST_DATA_2)

    CLIENT.copy_from_to(bucket_from=BUCKET,
                        measurement_from=TEST_DATA_2['measurement'],
                        devid_from=TEST_DATA_2['device_id'],
                        bucket_to=BUCKET,
                        measurement_to=TEST_DATA_1['measurement'],
                        devid_to=TEST_DATA_1['device_id'])

    data_merged = CLIENT.get_data_from_device_id(bucket=BUCKET,
                                                 measurement=TEST_DATA_1['measurement'],
                                                 device_id=TEST_DATA_1['device_id'])
    for i, data in  enumerate(TEST_DATA_1['values'] + TEST_DATA_2['values']):
        assert str(data[0]) == data_merged['values'][i][0]
        assert data[1] == data_merged['values'][i][1]
