FROM python:2.7

EXPOSE 5000
COPY . /app
WORKDIR /app

ENV http_proxy http://10.244.16.10:9090
ENV https_proxy https://10.244.16.10:9090

RUN pip install -r requirements.txt
RUN python -m spacy download fr
ENTRYPOINT ["python"]
CMD ["src/app.py"]