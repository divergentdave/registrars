#!/bin/bash
set -e

(cd lambda && python -m registrars.build)
docker build -t libspatialindex --file Dockerfile.libspatialindex .
docker run -v "$(pwd)/lambda/lib:/target" libspatialindex
PYTHONPATH=. sam build --template template-dev.yaml
