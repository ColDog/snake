VERSION := $(shell cat version)
COMMIT := $(shell git rev-parse --short HEAD)

run:
	cd src/ && python main.py
.PHONY: run

test:
	cd src/ && pytest $(ARGS)
.PHONY: test

lint:
	flake8 src/
.PHONY: lint

build:
	docker build -t coldog/snake:$(COMMIT) .
	docker tag coldog/snake:$(COMMIT) coldog/snake:latest
	docker tag coldog/snake:$(COMMIT) coldog/snake:$(VERSION)
	docker push coldog/snake:$(COMMIT)
	docker push coldog/snake:$(VERSION)
	docker push coldog/snake:latest
.PHONY: build

render:
	@cat manifest.yaml | sed "s/VERSION/$(VERSION)/" | sed "s/COMMIT/$(COMMIT)/"
.PHONY: render

deploy:
	make render | kubectl apply -f -
.PHONY: deploy

delete:
	make render | kubectl delete -f -
.PHONY: delete

external-ip:
	@kubectl get svc/snake-$(VERSION) -o json | jq -r '.status.loadBalancer.ingress[0].ip'
.PHONY: external-ip

release: build deploy external-ip
.PHONY: release
