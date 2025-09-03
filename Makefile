# Developer shortcuts
.PHONY: mock-up mock-down test-contract

mock-up:
	docker compose -f docker-compose.mock.yml up --build -d

mock-down:
	docker compose -f docker-compose.mock.yml down --volumes

test-contract: mock-up
	pytest -q tests/test_mcp_contract.py::test_mcp_contract
	$(MAKE) mock-down
