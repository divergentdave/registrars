#!/bin/bash
set -e

(cd lambda && python -m registrars.build)
PYTHONPATH=. sam build --template template-dev.yaml
