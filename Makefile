.PHONY: setup pipeline dashboard

setup:
	pip install --upgrade pip
	pip install -r requirements.txt

pipeline:
	python src/db/schema.py
	cd src/db && python load.py
	python src/analysis/frequencies.py
	python src/analysis/plots.py
	python src/analysis/stats.py
	python src/analysis/subset_analysis.py

dashboard:
	@echo "Dashboard not yet implemented."
