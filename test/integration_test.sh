#!/bin/bash
set -e
request=$(sam local generate-event apigateway aws-proxy --body '{"longitude":-93.3,"latitude":45.0}' --stage prod --method POST --path / --account-id 300689510484 --dns-suffix ca-central-1.amazonaws.com)
response=$(echo $request | sam local invoke --event -)
echo $response
echo $response | grep -q '"statusCode":"200"'
echo $response | grep -q '\\"https://gis.hennepin.us/property/map/default.aspx?C=476355.4109102419,4982994.171200306\\u0026L=7\\"'
