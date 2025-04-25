OLLAMA_MODELS = qwen2.5-coder:7b-instruct qwen2.5-coder:7b-instruct-q4_0
SELECTED_MODEL = qwen2.5-coder:7b-instruct 

PROJECT_DIR = $(QUIZ_PROJECT_DIR)
VENV_DIR = $(OLLAMA_VENV_DIR)
PYTHON_VERSION = 3.11

check_and_setup_ollama:
	@echo "Checking if Ollama is installed..."
	@if ! command -v ollama >/dev/null 2>&1; then \
		echo "Ollama not found. Installing..."; \
		curl -fsSL https://ollama.com/install.sh | sh; \
		echo "Starting Ollama service..."; \
		sudo systemctl start ollama.service || true; \
	else \
		echo "Ollama is already installed"; \
		sudo systemctl restart ollama.service || true; \
	fi
	@echo "Checking and pulling required models..."
	@for model in $(OLLAMA_MODELS); do \
		if ! ollama list | grep -q "$$model"; then \
			echo "Pulling $$model..."; \
			ollama pull $$model; \
		else \
			echo "Model $$model is already installed"; \
		fi; \
	done
	@echo "Ollama setup complete!"

run_quiz_generator:
	@echo "Navigating to project directory..."
	@cd $(PROJECT_DIR) || (echo "Project directory not found!" && exit 1)
	@echo "Checking for virtual environment..."
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "Virtual environment not found. Creating one with Python $(PYTHON_VERSION)..."; \
                apt install -y python3.11-venv; \
		python$(PYTHON_VERSION) -m venv $(VENV_DIR) || (echo "Failed to create virtual environment. Is Python $(PYTHON_VERSION) installed?" && exit 1); \
		echo "Installing requirements..."; \
		. $(VENV_DIR)/bin/activate && pip install -r requirements.txt || true; \
	else \
		echo "Virtual environment found at $(VENV_DIR)"; \
	fi
	@echo "Running quiz generator script..."
	@cd $(PROJECT_DIR) && . $(VENV_DIR)/bin/activate && SELECTED_MODEL=$(SELECTED_MODEL) python python_quiz_gen.py
	@echo "Quiz generation complete!"


setup_and_run: check_and_setup_ollama run_quiz_generator git_push

git_push:
	git add .
	git commit -m "update run via makefile"
	git push
