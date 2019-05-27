#!/bin/bash
set -e
sam package --output-template-file packaged.yaml --s3-bucket divergentdave-registrars
sam deploy --template-file packaged.yaml --stack-name registrars --capabilities CAPABILITY_IAM
