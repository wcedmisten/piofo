FROM python:3.8-slim-buster

RUN apt-get update \
    && apt-get -y install \
    exiftool \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]