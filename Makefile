VERSION := $(shell git rev-parse --short HEAD)

run:
	cd src/ && python main.py

test:
	cd src/ && pytest $(ARGS)

lint:
	flake8 src/

build:
	docker build -t coldog/snake:$(VERSION) .
	docker tag coldog/snake:$(VERSION) coldog/snake:latest
	docker push coldog/snake:$(VERSION)
	docker push coldog/snake:latest

deploy:
	cat manifest.yaml | sed "s/VERSION/$(VERSION)/" | kubectl apply -f -

restart:
	kubectl get pods -o json | jq -r '.items[].metadata.name' | grep snake | xargs kubectl delete pod

rollback:
	kubectl rollout undo deployments/snake

external-ip:
	@kubectl get svc/snake -o json | jq -r '.status.loadBalancer.ingress[0].ip'
