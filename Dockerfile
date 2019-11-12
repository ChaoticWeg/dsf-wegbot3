FROM python:3.6

LABEL maintainer="shawn@chaoticweg.cc"
LABEL version="3.1.0"
LABEL description="weg's idiot son"

WORKDIR /src

# copy in requirements.txt and install
COPY requirements.txt /src
COPY Makefile /src
RUN make install

# copy in files
COPY . /src

ENTRYPOINT ["python", "run.py"]
