#!/bin/bash
if [ ! -f .aws-sam/build/template.yaml ]; then
    echo "Run build_lambda_prod.sh before deploying" 1>&2
    exit 1
fi
if grep -q "localhost\|127.0.0.1" .aws-sam/build/template.yaml; then
    echo "Run build_lambda_prod.sh before deploying" 1>&2
    exit 1
fi
set -e
sam package --output-template-file packaged.yaml --s3-bucket divergentdave-registrars
sam deploy --template-file packaged.yaml --stack-name registrars --capabilities CAPABILITY_IAM
