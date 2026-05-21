from unittest.mock import patch

import pytest


def _build_event(query_params=None):
    return {
        "httpMethod": "GET",
        "path": "/import",
        "queryStringParameters": query_params,
        "headers": {},
        "requestContext": {
            "stage": "prod",
            "requestId": "test-id",
        },
        "body": None,
        "isBase64Encoded": False,
    }


@pytest.mark.parametrize("query_params", [None, {"name": ""}])
def test_empty_name_invalid_name(query_params, import_products_file_mod):
    mod = import_products_file_mod
    with patch.object(mod, "s3_client"):
        event = _build_event(query_params=query_params)
        response = mod.handler(event, {})

    assert response["statusCode"] == 400


def test_success(import_products_file_mod):
    mod = import_products_file_mod
    expected_url = "https://signed-url"
    with patch.object(mod, "s3_client") as mock_s3:
        mock_s3.generate_presigned_url.return_value = expected_url

        event = _build_event(query_params={"name": "test.csv"})
        response = mod.handler(event, {})

    assert response["statusCode"] == 200
    assert response["body"] == expected_url


def test_s3_error(import_products_file_mod):
    mod = import_products_file_mod
    with patch.object(mod, "s3_client") as mock_s3:
        mock_s3.generate_presigned_url.side_effect = Exception("S3 error")

        event = _build_event(query_params={"name": "test.csv"})
        response = mod.handler(event, {})

    assert response["statusCode"] == 500
