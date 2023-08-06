import os
import boto3
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # run the .env file that contains environment variable definitions

try:
    DATA_DIR = Path(__file__).parent / 'data'
    assert DATA_DIR.is_dir()
except NameError:
    DATA_DIR = Path.cwd() / 'mathtext' / 'data'  
except AssertionError:
    try:
        DATA_DIR = Path(__file__).parent.parent / 'data'
        assert DATA_DIR.is_dir()
    except AssertionError:
        DATA_DIR = Path.cwd() / 'data'

if not DATA_DIR.is_dir():
    DATA_DIR = DATA_DIR.parent
if not DATA_DIR.is_dir():
    DATA_DIR = Path.cwd()  # worst case CWD should always exist
assert DATA_DIR.is_dir()  # without a DATA_DIR this package can't run

# Uploading dataset and model versions to object storage
OBJECT_STORAGE_ENDPOINT_URL=os.environ.get('OBJECT_STORAGE_ENDPOINT_URL')
OBJECT_STORAGE_REGION_NAME=os.environ.get('OBJECT_STORAGE_REGION_NAME')
OBJECT_STORAGE_AWS_ACCESS_KEY_ID=os.environ.get('OBJECT_STORAGE_AWS_ACCESS_KEY_ID')
OBJECT_STORAGE_AWS_SECRET_ACCESS_KEY=os.environ.get('OBJECT_STORAGE_AWS_SECRET_ACCESS_KEY')
OBJECT_STORAGE_NAME=os.environ.get('OBJECT_STORAGE_NAME')

# Download link for most current model
CURRENT_MODEL_VERSION=os.environ.get('CURRENT_MODEL_VERSION')
CURRENT_MODEL_FILENAME=os.environ.get('CURRENT_MODEL_FILENAME')
CURRENT_MODEL_LINK=f"{CURRENT_MODEL_VERSION}/{CURRENT_MODEL_FILENAME}"

# Public Google Sheet Id 
CSV_GOOGLE_SHEET_ID=os.environ.get('CSV_GOOGLE_SHEET_ID')
GOOGLE_SHEET_LINK = f"https://docs.google.com/spreadsheets/d/{CSV_GOOGLE_SHEET_ID}/export?format=csv"

TOKENS2INT_ERROR_INT = 32202


def set_client_session():
    session = boto3.session.Session()

    # Create a connection to the Space
    client = session.client(
        's3',
        endpoint_url=OBJECT_STORAGE_ENDPOINT_URL,
        region_name=OBJECT_STORAGE_REGION_NAME,
        aws_access_key_id=OBJECT_STORAGE_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=OBJECT_STORAGE_AWS_SECRET_ACCESS_KEY
    )
    return client


CLIENT = set_client_session()

