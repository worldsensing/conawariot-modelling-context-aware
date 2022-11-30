FROM python:3.9.5-slim-buster AS build

COPY ./requirements/common.txt common.txt
COPY ./requirements/dev.txt requirements.txt

RUN apt-get update &&  \
    apt-get -y --no-install-recommends install \
        # psycopg2
        gcc

RUN pip install -r ./requirements.txt --no-cache-dir --user

FROM python:3.9.5-slim-buster

WORKDIR /opt/cloud_api

# Recover information from first multi-stage build
COPY --from=build /root/.local /usr/local

# copy project source
RUN mkdir -p source/
COPY source source

COPY tests tests
COPY .coveragerc .
COPY pytest.ini .
RUN mkdir -p ./reports

# copy scripts
COPY scripts/run_tests.sh run_tests.sh

EXPOSE 5000
CMD ["sh", "/opt/cloud_api/run_tests.sh"]