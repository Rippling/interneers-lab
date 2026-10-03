-include .env.local


.tidy:
	go mod tidy

.setup-env:
	cp .env.sample .env.local

setup: .tidy .setup-env


.PHONY: .build
.build:
	go build -o bin/app cmd/app/main.go

run:
	./bin/app

build-and-run: .build run



test:
	curl http://localhost:${APP_PORT}/hello-world

welcome:
	curl -G "http://localhost:${APP_PORT}/hello" --data-urlencode "name=$(filter-out $@,$(MAKECMDGOALS))"



mongo-login:
	mongosh --host 127.0.0.1 --port ${MONGO_PORT} --username ${MONGO_USER} --password --authenticationDatabase admin
# Catch-all target to handle positional arguments (prevents "No rule to make target" error)
%:
	@:
