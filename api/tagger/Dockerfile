FROM python:3.5

EXPOSE 5000
COPY . /app
WORKDIR /app

ENV http_proxy http://10.244.16.10:9090
ENV https_proxy https://10.244.16.10:9090

RUN pip install -r requirements.txt
RUN python -m spacy download fr
ENTRYPOINT ["python"]
CMD ["app.py"]