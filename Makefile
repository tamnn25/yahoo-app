.PHONY: run venv install

ENV_NAME = .venv

venv:
	@if [ ! -d "$(ENV_NAME)" ]; then \
		python3 -m venv $(ENV_NAME); \
		echo "✅ Virtual environment created"; \
	else \
		echo "⚡ Virtual environment exists"; \
	fi

install: venv
	@source $(ENV_NAME)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run: install
	@source $(ENV_NAME)/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
