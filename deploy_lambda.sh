#!/bin/bash
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket divergentdave-registrars
sam deploy --template-file packaged.yaml --stack-name registrars --capabilities CAPABILITY_IAM
aws cloudformation describe-stacks --stack-name registrars --query 'Stacks[].Outputs[?OutputKey=`RegistrarsApi`]' --output table
