FROM python:3.8

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install git openssh-client

RUN pip install tox

ARG TERRAFORM_VERSION=1.1.6
RUN curl -sSLo terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && install terraform /usr/local/bin \
 && rm -rf terraform_${TERRAFORM_VERSION}_linux_amd64.zip terraform
