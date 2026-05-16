.PHONY: setup pipeline dashboard

setup:
	pip install --upgrade pip
	pip install -r requirements.txt
	python src/db/schema.py

pipeline:
	@echo "Pipeline not yet implemented."

dashboard:
	@echo "Dashboard not yet implemented."
