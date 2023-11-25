FROM python:3.9.18-slim-bullseye

RUN useradd -ms /bin/bash whisperx
USER whisperx

WORKDIR /app

COPY --chown=whisperx:whisperx . /app

RUN sh setup.sh


