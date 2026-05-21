#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess

import aws_cdk as cdk

from stacks.product_stack import InfraStack

packages = {
    "product-service-common": "services/common",
    "product-service-create": "services/create",
    "product-service-get-by-id": "services/get_by_id",
    "product-service-get-list": "services/get_list",
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
InfraStack(app, "ProductServiceStack", env={"region": "eu-central-1"})

app.synth()

for pkg_name, path in packages.items():
    file = Path(path) / "requirements.txt"
    file.unlink()
