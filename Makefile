PYTHON ?= python3
VENV ?= .venv
ACTIVATE = source $(VENV)/bin/activate

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

$(VENV)/bin/python:
	$(PYTHON) -m venv $(VENV)

install: $(VENV)/bin/python
	$(ACTIVATE) && pip install -U pip && pip install -r requirements.txt

install-dev: $(VENV)/bin/python
	$(ACTIVATE) && pip install -U pip && pip install -r requirements-dev.txt

fmt:
	$(ACTIVATE) && black src tests demos

lint:
	$(ACTIVATE) && ruff check src tests demos

test:
	$(ACTIVATE) && pytest

demo:
	$(ACTIVATE) && python -m demos.run_pattern --pattern prompt_chaining --mock

gradio:
	$(ACTIVATE) && python -m demos.gradio_interface

clean:
	rm -rf $(VENV) build dist *.egg-info
