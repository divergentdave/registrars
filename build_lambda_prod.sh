#!/bin/bash
set -e

(cd lambda && python -m registrars.build)
docker build -t libspatialindex --file Dockerfile.libspatialindex .
docker run -v "$(pwd)/lambda/lib:/target" libspatialindex
sam build
(cd .aws-sam/build/RegistrarsAppFunction/lib/ &&
    ln -s libspatialindex.so.4.0.1 libspatialindex.so &&
    ln -s libspatialindex_c.so.4.0.1 libspatialindex_c.so)
