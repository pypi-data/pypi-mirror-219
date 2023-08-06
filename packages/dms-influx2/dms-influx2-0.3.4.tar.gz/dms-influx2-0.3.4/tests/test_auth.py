import os
import pytest
from influxdb_client.rest import ApiException

from dms_influx2.lib import DmsInflux2

DATABASE_URL = os.environ['DATABASE_URL']
TOKEN = os.environ['TOKEN']
ORG = os.environ['ORG']
BUCKET = 'test_bucket'
CLIENT = DmsInflux2(url=DATABASE_URL, token=TOKEN, org=ORG)


def test_bucket_exists():
    if CLIENT.buckets_api().bucket_exists(BUCKET):
        CLIENT.buckets_api().delete_bucket_by_name(BUCKET)
    CLIENT.buckets_api()._create_bucket(bucket_name=BUCKET)
    assert CLIENT.buckets_api().bucket_exists(BUCKET)


def test_delete_authorization():
    auth = CLIENT.authorizations_api().create_bucket_authorization(bucket_name=BUCKET, org_name=ORG)
    assert len(auth.id) > 5

    assert CLIENT.authorizations_api().delete_authorization(auth) is None

    with pytest.raises(ApiException):
        CLIENT.authorizations_api().find_authorization_by_id(auth_id=auth.id)

# # # TODO fix this test
# def test_create_bucket_with_token_and_delete_permissions():
#     """Test create new bucket with auth token and check for writes/reads permissions"""
#
#     new_token = client.buckets_api().create_bucket_with_auth(bucket_name=bucket).token
#
#     measurement = "test"
#
#     client2 = DmsInflux2(url=url, token=new_token, org=org)
#     data = {
#         "measurement": measurement,
#         "device_id": "test.ch",
#         "values": [(datetime.utcnow(), 0)]
#     }
#     client2.save_data(bucket=bucket, data=data)
#     client.delete_api().delete_data(bucket=bucket, measurements=[measurement])
#
#     client.buckets_api().delete_permissions(bucket_name=bucket)
#     data = {
#         "measurement": measurement,
#         "device_id": "test.ch",
#         "values": [(datetime.utcnow(), 0)]
#     }
#     with pytest.raises(Exception):
#         client2.save_data(bucket=bucket, data=data)
