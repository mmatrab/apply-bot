FROM python:3.8

USER root

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
RUN mkdir -p workspaces/tests
COPY . workspaces/tests/
WORKDIR workspaces/tests
