FROM python:3.6

LABEL maintainer="shawn@chaoticweg.cc"
LABEL version="3.0.2"
LABEL description="weg's idiot son"

WORKDIR /src

# copy in requirements.txt and install
COPY requirements.txt /src
COPY Makefile /src
RUN make install

# copy in files
COPY . /src

# define entry point
ENTRYPOINT ["python", "run.py"]
