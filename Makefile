PYTHON ?= $(shell command -v python3 || command -v python)
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: help install install-dev fmt lint test demo gradio clean

help:
	@echo "Targets:"
	@echo "  make install      # create venv and install runtime deps"
	@echo "  make install-dev  # create venv and install dev deps"
	@echo "  make fmt          # run code formatters"
	@echo "  make lint         # run ruff checks"
	@echo "  make test         # run pytest suite"
	@echo "  make demo         # run CLI demo with mock LLM"
	@echo "  make gradio       # launch Gradio interface"

$(VENV)/pyvenv.cfg:
	$(PYTHON) -m venv $(VENV)
	@echo "created venv at $(VENV) using $(PYTHON)"

install: $(VENV)/pyvenv.cfg
	@# Ensure pip exists inside the venv; some Python installs create venvs without pip
	@if [ ! -x "$(PIP)" ]; then \
		echo "pip not found in $(VENV); attempting to bootstrap pip..."; \
		$(PY) -m ensurepip --upgrade 2>/dev/null || true; \
		$(PY) -m pip install --upgrade pip setuptools wheel 2>/dev/null || true; \
		if [ ! -x "$(PIP)" ]; then \
			echo "Bootstrapping pip failed; re-creating venv using $(PYTHON)"; \
			$(PYTHON) -m venv --upgrade-deps $(VENV) 2>/dev/null || $(PYTHON) -m venv $(VENV); \
		fi; \
	fi
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

install-dev: $(VENV)/pyvenv.cfg
	@# Ensure pip exists inside the venv (see install target)
	@if [ ! -x "$(PIP)" ]; then \
		echo "pip not found in $(VENV); attempting to bootstrap pip..."; \
		$(PY) -m ensurepip --upgrade 2>/dev/null || true; \
		$(PY) -m pip install --upgrade pip setuptools wheel 2>/dev/null || true; \
		if [ ! -x "$(PIP)" ]; then \
			echo "Bootstrapping pip failed; re-creating venv using $(PYTHON)"; \
			$(PYTHON) -m venv --upgrade-deps $(VENV) 2>/dev/null || $(PYTHON) -m venv $(VENV); \
		fi; \
	fi
	$(PIP) install -U pip
	$(PIP) install -r requirements-dev.txt

fmt: $(VENV)/pyvenv.cfg
	$(PY) -m black src tests demos

lint: $(VENV)/pyvenv.cfg
	$(PY) -m ruff check src tests demos

test: $(VENV)/pyvenv.cfg
	$(PY) -m pytest

demo: $(VENV)/pyvenv.cfg
	$(PY) -m demos.run_pattern --pattern prompt_chaining --model mock

gradio: $(VENV)/pyvenv.cfg
	$(PY) -m demos.gradio_interface

clean:
	rm -rf $(VENV) build dist *.egg-info
