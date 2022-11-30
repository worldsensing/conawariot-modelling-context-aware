FROM python:3.9.15-slim-buster AS build

COPY ./requirements/common.txt requirements.txt

RUN apt-get update &&  \
    apt-get -y --no-install-recommends install \
        # psycopg2
        gcc

RUN pip install -r ./requirements.txt --no-cache-dir --user

FROM python:3.9.15-slim-buster

WORKDIR /opt/cloud_api

# Recover information from first multi-stage build
COPY --from=build /root/.local /usr/local

RUN mkdir -p source/
COPY source source
COPY scripts/run_app.sh run_app.sh

CMD ["sh", "/opt/cloud_api/run_app.sh"]