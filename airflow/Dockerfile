FROM python:3.6-jessie

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux 

# Airflow
ARG AIRFLOW_VERSION=1.9.0
ARG AIRFLOW_HOME=/usr/local/airflow

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
#ENV http_proxy http://10.244.16.10:9090
#ENV https_proxy https://10.244.16.10:9090

COPY ./requirements.txt /requirements.txt
COPY ./script/ /script

RUN set -ex \
    && buildDeps=' \
        python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        build-essential \
        libblas-dev \
        liblapack-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        python3-pip \
        git \
        python3-requests \
        mysql-client \
        mysql-server \
        #default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install Cython \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install -r requirements.txt \
    && pip install apache-airflow[celery,postgres,hive,hdfs,jdbc] \
    && pip install celery[redis]==4.1.1 \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge -yqq $buildDeps libpq-dev \  
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN apt-get update && apt-get install -y git

COPY airflow.cfg /usr/local/airflow/airflow.cfg
COPY script/entrypoint.sh /entrypoint.sh

RUN pip install -r /requirements.txt
RUN python -m spacy download fr
RUN chown -R airflow: /usr/local/airflow

EXPOSE 8080 5555 8793 5432 6379

USER airflow
WORKDIR /usr/local/airflow
ENTRYPOINT ["sh", "/script/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint