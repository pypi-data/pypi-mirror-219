"""  This file is run when the model is created in multilabel_intent_recognition.py.  

It automatically uploads as public files the most recent model and dataset to an object storage service (Digital Ocean Spaces).
"""

import boto3
import botocore
import mimetypes
import os
import re
from datetime import datetime

from mathtext.constants import OBJECT_STORAGE_NAME, CLIENT


def get_object_store_buckets(client, bucket_name):
    """ Returns a list of folders in the object storage 
    
    Output
    ['v0/', 'v0/multi_intent_recognizer_20230325.joblib', 'v0/rori_labeled_data_20230325.csv', 'v1/model_context_20230518.txt', 'v1/multi_intent_recognizer_20230518.pkl', 'v1/rori_multilabeled_data_20230518.csv']
    """
    try:
        response = client.list_objects_v2(Bucket=bucket_name)
    except:
        print(f"Bucket '{bucket_name}' does not exist.")

    # Filter through response object for folder names
    objs = [obj['Key'] for obj in response['Contents']]
    return objs


def find_current_max_version(buckets):
    """ Searches through the object storage folders to find the most recent model version and set the next version
    
    >>> find_current_max_version(['v0/', 'v0/multi_intent_recognizer_20230325.joblib', 'v0/rori_labeled_data_20230325.csv', 'v1/model_context_20230518.txt', 'v1/multi_intent_recognizer_20230518.pkl', 'v1/rori_multilabeled_data_20230518.csv'])
    1, 2
    """
    current_version = -1

    for obj in buckets:
        try:
            result = re.search(r'v(\d+)', obj)
            match = int(result.group(1))
        except:
            continue

        if match > current_version:
            current_version = match
    next_version = current_version + 1
    return current_version, next_version


def upload_file(client, file_path, bucket_name, spaces_path):
    """ Uploads a local file to the object storage """
    client.upload_file(
        file_path,
        bucket_name,
        spaces_path,
        ExtraArgs={'ACL': 'public-read'}
    )


def upload_to_object_storage(
    csv_path,
    model_requirements_path,
    model_path
):
    client = CLIENT
    bucket_name = OBJECT_STORAGE_NAME
    buckets = get_object_store_buckets(client, bucket_name)
    current_version, next_version = find_current_max_version(buckets)
    current_date = datetime.now().strftime('%Y%m%d')

    dataset_file_name = f'rori_multilabeled_data_{current_date}.csv'
    model_requirements_name = f'model_context_{current_date}.txt'
    model_file_name = f'multi_intent_recognizer_{current_date}.pkl'

    # Uploads the CSV - Not a local file
    client.upload_fileobj(
        csv_path,
        bucket_name,
        f'v{next_version}/{dataset_file_name}',
        ExtraArgs={'ACL': 'public-read'}
    )

    # Uploads model dev context - Local file
    upload_file(
        client,
        str(model_requirements_path),
        bucket_name,
        f'v{next_version}/{model_requirements_name}'
    )

    # Uploads the model - Local file
    upload_file(
        client,
        str(model_path),
        bucket_name,
        f'v{next_version}/{model_file_name}'
    )

    print(f"""
    Upload to Object Storage Successful!

    Remember to update the .env variables with the most current model in the production and staging servers.

    CURRENT_MODEL_LINK='v{next_version}/{model_file_name}'
    CURRENT_MODEL_FILENAME='{model_file_name}'
    """)
    return {
        'model_version': next_version,
        'model': model_file_name,
        'dataset': dataset_file_name
    }
