FROM python:2.7

EXPOSE 5000
COPY . /app
WORKDIR /app

ENV http_proxy http://10.244.16.10:9090
ENV https_proxy https://10.244.16.10:9090

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
    rm -rf /tmp/fastText/.git* && \
    mv /tmp/fastText/* / && \
    cd / && \
    make

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install -r requirements.txt
RUN python -m spacy download en_vectors_web_lg
RUN python -m spacy download fr
ENTRYPOINT ["python"]
CMD ["src/app.py"]