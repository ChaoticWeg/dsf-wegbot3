FROM python:3.6-alpine

LABEL maintainer="shawn@chaoticweg.cc"
LABEL version="3.0"
LABEL description="wegbot version 3 (discord.py)"

WORKDIR /src
COPY . /src

RUN pip install -r requirements.txt
CMD python run.py
