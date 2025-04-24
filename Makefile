.PHONY: all clean install-free install-forewarn test-free test-forewarn deploy

# Default target
all: install-free install-forewarn

# Clean build artifacts
clean:
	rm -rf */__pycache__
	rm -rf */.pytest_cache
	rm -rf */results
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Free API Version
install-free:
	cd free_api && pip install -r requirements.txt

test-free:
	cd free_api && python -m pytest test_free_verification.py -v
	cd free_api && python test_numverify.py

# Forewarn Version
install-forewarn:
	cd forewarn && pip install -r requirements.txt

test-forewarn:
	cd forewarn && python -m pytest test_lead_verification.py -v

# Deployment (both versions)
deploy:
	vercel --prod

# Development
dev-free:
	cd free_api && python -m flask run

dev-forewarn:
	cd forewarn && python -m flask run

# Help
help:
	@echo "Available targets:"
	@echo "  all              - Install both versions"
	@echo "  clean            - Remove build artifacts"
	@echo "  install-free     - Install free API version"
	@echo "  install-forewarn - Install Forewarn version"
	@echo "  test-free        - Run tests for free API version"
	@echo "  test-forewarn    - Run tests for Forewarn version"
	@echo "  deploy           - Deploy both versions to Vercel"
	@echo "  dev-free         - Run free API version in development"
	@echo "  dev-forewarn     - Run Forewarn version in development" 