#!/usr/bin/env bash
docker build -t dsf-wegbot3 . && docker run -v "$(HOME)/.dsf-wegbot":/root/.dsf-wegbot --name dsf-wegbot3 dsf-wegbot3
