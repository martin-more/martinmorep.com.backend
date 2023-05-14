import os

import boto3

OPERATION_PUT_OBJECT = "put_object"
OPERATION_GET_OBJECT = "get_object"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class S3Client:
    def __init__(
        self,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    ):
        self._client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="us-east-2",
        )

    def create_presigned_url(
        self,
        bucket_name,
        object_name,
        expiration_time=3600,
        content_type=None,
        operation_name=OPERATION_PUT_OBJECT,
    ):
        params = {"Bucket": bucket_name, "Key": object_name}
        if content_type:
            params.update({"ContentType": content_type})

        return self._client.generate_presigned_url(
            ClientMethod=operation_name, Params=params, ExpiresIn=expiration_time
        )
