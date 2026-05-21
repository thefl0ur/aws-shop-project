import importlib.util
import os
import sys
from pathlib import Path

import boto3
import pytest
from moto import mock_aws

os.environ["BUCKET_NAME"] = "test-bucket"

SERVICES_DIR = Path(__file__).parent.parent / "services"
COMMON_PATH = str(SERVICES_DIR / "common")
IMPORT_PRODUCTS_FILE_PATH = str(SERVICES_DIR / "import_products_file" / "main.py")
IMPORT_FILE_PARSER_PATH = str(SERVICES_DIR / "import_file_parser" / "main.py")


@pytest.fixture(scope="module", autouse=True)
def _add_common_path():
    if COMMON_PATH not in sys.path:
        sys.path.insert(0, COMMON_PATH)


@pytest.fixture
def import_products_file_mod():
    spec = importlib.util.spec_from_file_location(
        "import_products_file_app",
        IMPORT_PRODUCTS_FILE_PATH,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def import_file_parser_mod():
    spec = importlib.util.spec_from_file_location(
        "import_file_parser_app",
        IMPORT_FILE_PARSER_PATH,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def mock_s3():
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")
