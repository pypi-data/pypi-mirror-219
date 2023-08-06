# s3_operations.py
import boto3
from collections.abc import Generator

class S3Operations:
    #####################################################################
    def __get_client(
            self,
            access_key_id=None,
            secret_access_key=None
    ):
        session = boto3.Session()
        if access_key_id:
            s3_client = session.client(
                service_name='s3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key
            )
            print('NODD Authenticated')
        else:
            s3_client = session.client(service_name='s3')
        return s3_client

    #####################################################################
    def __chunked(
            self,
            ll: list,
            n: int
    ) -> Generator:
        """Yields successively n-sized chunks from ll.

        Parameters
        ----------
        ll : list
            List of all objects.
        n : int
            Chunk size to break larger list down from.

        Returns
        -------
        Batches : Generator
            Breaks the data into smaller chunks for processing
        """
        for i in range(0, len(ll), n):
            yield ll[i:i + n]

    #####################################################################
    def list_objects(  # analog to "find_children_objects"
            self,
            bucket_name,
            prefix,
            access_key_id=None,
            secret_access_key=None
    ):
        # Returns a list of key strings for each object in bucket defined by prefix
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        keys = []
        for page in s3_client.get_paginator('list_objects_v2').paginate(Bucket=bucket_name, Prefix=prefix):
            if 'Contents' in page.keys():
                # keys.extend(page['Contents'])
                keys.extend([k['Key'] for k in page['Contents']])
        print(f'Found {len(keys)} items')
        return keys

    #####################################################################
    def download_file(
            self,
            bucket_name,
            key,
            file_name,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        s3_client.download_file(Bucket=bucket_name, Key=key, Filename=file_name)

    #####################################################################
    def delete_object(
            self,
            bucket_name,
            key,
            access_key_id=None,
            secret_access_key=None
    ):
        print('key')
        print(key)
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        print(f"Deleting item: Bucket={bucket_name}, Key={key}")
        s3_client.delete_object(Bucket=bucket_name, Key=key)

    #####################################################################
    def upload_file(
            self,
            file_name,
            bucket_name,
            key,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        s3_client.upload_file(Filename=file_name, Bucket=bucket_name, Key=key)

    #####################################################################
