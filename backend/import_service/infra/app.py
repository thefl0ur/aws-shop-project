#!/usr/bin/env python3
from pathlib import Path
import subprocess

import aws_cdk as cdk

from stacks.import_product_stack import InfraStack


packages = {
    "import-products-file": "services/import_products_file",
    "import-products-common": "services/common",
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
InfraStack(app, "ImportServiceStack", env={"region": "eu-central-1"})

app.synth()

for pkg_name, path in packages.items():
    file = Path(path) / "requirements.txt"
    file.unlink()
