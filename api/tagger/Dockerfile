FROM python:3.6

EXPOSE 5000
COPY . /app
WORKDIR /app

#local proxy
#ENV http_proxy http://10.244.16.10:9090
#ENV https_proxy https://10.244.16.10:9090

#because else, textacy fail to install cld2-cffi to detect language
ENV CFLAGS "-Wno-narrowing"

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq gcc \
    build-essential \
    python \
    git \
    python-dev \
    python-pip \
    python-virtualenv \
    python3-dev \
    libkrb5-dev \
    libsasl2-dev \
    libssl-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    libpq-dev

RUN git clone https://github.com/facebookresearch/fastText.git /tmp/fastText && \
    cd /tmp/fastText && \
    pip install . && \
    cd /app && \
    mkdir -p /app/data

ADD https://s3.amazonaws.com/tagger-eig/models/models.tar.gz /app/data

RUN tar zxvf /app/data/models.tar.gz -C /app/data/ && \
    rm -f /app/data/models.tar.gz && \
    pip install -r requirements.txt && \
    python -m spacy download en_vectors_web_lg && \
    python -m spacy download fr

CMD ["python", "app.py"]