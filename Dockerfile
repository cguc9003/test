FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt ./
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
