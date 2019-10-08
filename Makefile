.PHONY: install deploy

install:
	pip install -r requirements.txt

deploy:
	docker build -t dsf-wegbot3 .
	-docker rm -f dsf-wegbot3
	docker run -it -v /home/weg/.dsf-wegbot:/root/.dsf-wegbot --name dsf-wegbot3 dsf-wegbot3

