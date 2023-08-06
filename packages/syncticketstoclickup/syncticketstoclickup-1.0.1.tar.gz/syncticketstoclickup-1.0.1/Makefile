# Create a virtual environment
venv:
	python3 -m venv .venv

# Install the required packages in the virtual environment
install: venv
	. .venv/bin/activate && pip install -r syncticketstoclickup/requirements.txt

# Run the script in the virtual environment
run: venv
	. .venv/bin/activate && python syncticketstoclickup/main.py

# Help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  venv      Create a virtual environment"
	@echo "  install   Install the required packages in the virtual environment"
	@echo "  run       Run the main.py script in the virtual environment"
	@echo "  help      Show this help message"