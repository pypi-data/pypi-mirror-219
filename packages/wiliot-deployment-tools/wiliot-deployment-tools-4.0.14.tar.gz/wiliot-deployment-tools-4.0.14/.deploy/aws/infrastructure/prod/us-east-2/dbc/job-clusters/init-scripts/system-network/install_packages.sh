#!/bin/bash
apt-get update && apt-get install curl unzip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

PACKAGES='wiliot-deployment-tools==4.0.10'

aws codeartifact login --tool pip --domain wiliot-cloud --domain-owner 096303741971 --repository pypi --region us-east-2

/databricks/python/bin/pip install --no-cache ${PACKAGES}
