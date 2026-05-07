set dotenv-load

infra-init path:
    mkdir -p {{path}}/infra && cd {{path}}/infra && cdk init app --language python
    cd {{path}}/infra && source .venv/bin/activate
    cd {{path}}/infra && pip install -r requirements.txt

infra-bootstrap path:
    cd {{path}}/infra && cdk bootstrap --profile $PROFILE

infra-deploy path:
    cd {{path}} && uv pip compile pyproject.toml -o src/requirements.txt
    cd {{path}}/infra && cdk deploy --profile $PROFILE --require-approval never

infra-destroy path:
    cd {{path}}/infra && cdk destroy --profile $PROFILE --force

infra-synt path:
    cd {{path}} && uv pip compile pyproject.toml -o src/requirements.txt
    cd {{path}}/infra && cdk synth --profile $PROFILE
    cd {{path}} && rm src/requirements.txt

run-sam path:
    cd {{path}} && sam local start-api -t infra/cdk.out/ProductServiceStack.template.json --profile $PROFILE