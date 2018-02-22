VERSION := $(shell cat version)

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
	docker build -t coldog/snake:$(VERSION) .
	docker tag coldog/snake:$(VERSION) coldog/snake:latest
	docker push coldog/snake:$(VERSION)
	docker push coldog/snake:latest
.PHONY: build

deploy:
	cat manifest.yaml | sed "s/VERSION/$(VERSION)/" | kubectl apply -f -
.PHONY: deploy

delete:
	cat manifest.yaml | sed "s/VERSION/$(VERSION)/" | kubectl delete -f -
.PHONY: delete

render:
	cat manifest.yaml | sed "s/VERSION/$(VERSION)/"
.PHONY: render

external-ip:
	@kubectl get svc/snake-$(VERSION) -o json | jq -r '.status.loadBalancer.ingress[0].ip'
.PHONY: external-ip
