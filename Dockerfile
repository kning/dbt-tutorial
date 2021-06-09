ARG BASE_IMAGE="python:3.8-slim-buster"

FROM $BASE_IMAGE
RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends \
    git \
    software-properties-common \
    make \
    build-essential \
    ca-certificates \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install --requirement ./requirements.txt
ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8
WORKDIR /usr/app

# copy dbt project 
COPY ./jaffle-shop/analysis ./analysis
COPY ./jaffle-shop/data ./data
COPY ./jaffle-shop/macros ./macros
COPY ./jaffle-shop/models ./models
COPY ./jaffle-shop/snapshots ./snapshots
COPY ./jaffle-shop/tests ./tests
COPY ./jaffle-shop/dbt_project.yml ./dbt_project.yml
COPY ./jaffle-shop/profiles.yml /root/.dbt/profiles.yml
