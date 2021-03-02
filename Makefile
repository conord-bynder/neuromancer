.PHONY: test
test:
	docker build --target Unittest .

.PHONY: lint
lint:
	docker build --target Lint .

.PHONY: mypy
mypy:
	docker build --target Mypy .

.PHONY: bandit
bandit:
	docker build --target Bandit .

.PHONY: build
build: test
