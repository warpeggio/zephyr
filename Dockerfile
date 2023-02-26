FROM python:3.7-slim-buster
RUN apt-get update -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["zephyr.py"]
