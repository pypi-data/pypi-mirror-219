import os

from dms_influx2.lib import DmsInflux2

DATABASE_URL = os.environ['DATABASE_URL']
TOKEN = os.environ['TOKEN']
ORG = os.environ['ORG']
BUCKET = 'test_bucket'
CLIENT = DmsInflux2(url=DATABASE_URL, token=TOKEN, org=ORG)

BUCKET_TEST = 'test_buckets'
BUCKET_TEST_DESCRIPTION = 'test_buckets'
BUCKET_TEST_DESCRIPTION_READONLY = 'test_buckets_readonly'
AUTH_BUCKET = 'test2'


def test_bucket_exists():
    CLIENT.authorizations_api().delete_all_bucket_authorizations()

    if CLIENT.buckets_api().bucket_exists(bucket_name=BUCKET_TEST):
        CLIENT.buckets_api().delete_bucket_by_name(bucket_name=BUCKET_TEST)

    if CLIENT.buckets_api().bucket_exists(bucket_name=AUTH_BUCKET):
        CLIENT.buckets_api().delete_bucket_by_name(bucket_name=AUTH_BUCKET)

    CLIENT.buckets_api()._create_bucket(bucket_name=BUCKET_TEST)
    assert CLIENT.buckets_api().bucket_exists(BUCKET_TEST)


def test_change_bucket_description():
    pass


def test_create_bucket_with_default_authorizations():
    CLIENT.buckets_api().delete_bucket_by_name(bucket_name=BUCKET_TEST)
    CLIENT.buckets_api().create_bucket_with_default_authorizations(BUCKET_TEST)

    auth_read_write = CLIENT.authorizations_api().find_authorizations_by_description(BUCKET_TEST)[0]
    assert auth_read_write.description == BUCKET_TEST
    assert len(auth_read_write.permissions) == 2
    assert auth_read_write.permissions[0].action == 'read'
    assert auth_read_write.permissions[0].resource.type == 'buckets'
    assert auth_read_write.permissions[1].action == 'write'
    assert auth_read_write.permissions[1].resource.type == 'buckets'

    auth_read = CLIENT.authorizations_api().find_authorizations_by_description(BUCKET_TEST_DESCRIPTION_READONLY)[0]
    assert auth_read.description == BUCKET_TEST_DESCRIPTION_READONLY
    assert len(auth_read.permissions) == 1
    assert auth_read.permissions[0].action == 'read'
    assert auth_read.permissions[0].resource.type == 'buckets'

    ### Remove this permissions and test get_or_create_bucket_authorization()
    print('auth read', auth_read)
    CLIENT.authorizations_api().delete_authorization(auth_read_write)
    CLIENT.authorizations_api().delete_authorization(auth_read)

    auth = CLIENT.authorizations_api().get_or_create_bucket_authorization(bucket_name=BUCKET_TEST, read_only=True)
    assert auth.description == BUCKET_TEST_DESCRIPTION_READONLY
    assert len(auth.permissions) == 1
    assert auth.permissions[0].action == 'read'
    assert auth.permissions[0].resource.type == 'buckets'

    auth = CLIENT.authorizations_api().get_or_create_bucket_authorization(bucket_name=BUCKET_TEST, read_only=False)
    print(auth)
    assert auth.description == BUCKET_TEST_DESCRIPTION
    assert len(auth.permissions) == 2
    assert auth.permissions[0].action == 'read'
    assert auth.permissions[0].resource.type == 'buckets'
    assert auth.permissions[1].action == 'write'
    assert auth.permissions[1].resource.type == 'buckets'

def test_auths_dict():
    auths = CLIENT.authorizations_api().get_bucket_authorizations_dict()
    print(auths)
    assert True

def test_buckets_dict():
    pass

# # # # TODO fix this test
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


def test_delete_bucket_by_name():
    if CLIENT.buckets_api().bucket_exists(bucket_name=BUCKET_TEST):
        CLIENT.buckets_api().delete_bucket_by_name(bucket_name=BUCKET_TEST)

    if CLIENT.buckets_api().bucket_exists(bucket_name=AUTH_BUCKET):
        CLIENT.buckets_api().delete_bucket_by_name(bucket_name=AUTH_BUCKET)


    assert not CLIENT.buckets_api().bucket_exists(BUCKET_TEST)
    assert not CLIENT.buckets_api().bucket_exists(AUTH_BUCKET)
