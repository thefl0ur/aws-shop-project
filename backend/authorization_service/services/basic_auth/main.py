import base64
import os
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))

    auth_header: str = event.get("authorizationToken")

    if not auth_header or not auth_header.lower().startswith("basic "):
        raise Exception("Unauthorized")

    try:
        _, encoded_token = auth_header.split(" ")
        decoded_tocken = base64.b64decode(encoded_token).decode("utf-8")
        username, password = decoded_tocken.split(":", 1)
    except Exception:
        logger.error("Failed to parse token")
        raise Exception("Unauthorized")

    expected_password = os.environ.get(username)
    is_authorized = (expected_password is not None) and (expected_password == password)

    resource = event.get("methodArn")
    effect = "Allow" if is_authorized else "Deny"

    policy = generate_policy(principal_id=username, effect=effect, resource=resource)

    return policy


def generate_policy(principal_id, effect, resource):
    auth_response = {"principalId": principal_id}

    if effect and resource:
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
            ],
        }
        auth_response["policyDocument"] = policy_document

    return auth_response
