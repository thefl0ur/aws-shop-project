#!/usr/bin/env python3
import subprocess

from pathlib import Path

import aws_cdk as cdk

from stack.auth_stack import AuthorizationServiceStack

packages = {
    "basic-auth-service": "services/basic_auth",
}

for pkg_name, path in packages.items():
    subprocess.run(
        [
            "uv",
            "export",
            "--frozen",
            "--no-dev",
            "--package",
            pkg_name,
            "-o",
            f"{path}/requirements.txt",
        ],
        check=True,
    )
app = cdk.App()
AuthorizationServiceStack(
    app, "AuthorizationServiceStack", env={"region": "eu-central-1"}
)

app.synth()

for pkg_name, path in packages.items():
    file = Path(path) / "requirements.txt"
    file.unlink()
