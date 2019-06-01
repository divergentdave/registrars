# Registrars

This repository holds the source code and data for
https://davidsherenowitsa.party/registrars, a serverless, single-page web app.
The web app takes in a location, and displays links to online property maps of
various localities.

## Development

This is a polyglot project, with multiple dependencies. Development will
require [Python 3](https://www.python.org/), [Node](https://nodejs.org/),
Docker, and many packages from PyPI and NPM. To get started, clone this
repository, [create and activate a Python
virtualenv](https://virtualenv.pypa.io/en/stable/), and run the following
commands.

```bash
pip install -r requirements-dev.txt
npm install
```

The rest of the development workflow is encapsulated in the following shell
scripts, from building artifacts, to running the whole app locally, to
deploying.

```bash
./build_lambda_dev.sh
./run_lambda_dev.sh
./run_webapp_dev.sh

./build_lambda_prod.sh
./build_webapp_prod.sh
./deploy_lambda.sh
./deploy_webapp.sh
```

An AWS access key is required for validating the CloudFormation template and
deploying the app. To do either of these, create an access key, and provide it
to the AWS SDK through environment variables or configuration files.
