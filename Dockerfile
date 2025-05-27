FROM python:3.10-slim-bullseye

WORKDIR /textanalyzer

COPY . /textanalyzer

RUN pip install .