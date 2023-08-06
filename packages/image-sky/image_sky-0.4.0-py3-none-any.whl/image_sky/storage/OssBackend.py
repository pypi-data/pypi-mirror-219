#
# Copyright 2018 PyWren Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from .exceptions import StorageNoSuchKeyError
import oss2

class OssBackend(object):
    """
    A wrap-up around S3 boto3 APIs.
    """

    def __init__(self, s3config):
        self.s3_bucket = s3config['bucket']
        self.endpoint = s3config['endpoint']
        self.auth = oss2.Auth(s3config['access_key_id'], s3config['access_key_secret'])
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.s3_bucket)

    def put_object(self, key, data):
        """
        Put an object in S3. Override the object if the key already exists.
        :param key: key of the object.
        :param data: data of the object
        :type data: str/bytes
        :return: None
        """
        self.bucket.put_object(key=key, data=data)

    def get_object(self, key):
        """
        Get object from S3 with a key. Throws StorageNoSuchKeyError if the given key does not exist.
        :param key: key of the object
        :return: Data of the object
        :rtype: str/bytes
        """
        try:
            result = self.bucket.get_object(key=key)
            data = result.read()
            return data
        except oss2.exceptions.NoSuchKey as e:
            if e.code == "NoSuchKey":
                raise StorageNoSuchKeyError(key)
            else:
                raise e

    def key_exists(self, key):
        """
        Check if a key exists in S3.
        :param key: key of the object
        :return: True if key exists, False if not exists
        :rtype: boolean
        """
        try:
            self.bucket.head_object(key=key)
            return True
        except oss2.exceptions.NotFound as e:
            if e.code == "NotFound":
                return False
            else:
                raise e

    def list_keys_with_prefix(self, prefix):
        """
        Return a list of keys for the given prefix.
        :param prefix: Prefix to filter object names.
        :return: List of keys in bucket that match the given prefix.
        :rtype: list of str
        """
        result = self.bucket.list_objects_v2(prefix)
        obj_list = result.object_list

        return [obj.key for obj in obj_list]
