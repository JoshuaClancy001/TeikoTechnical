.PHONY: setup pipeline dashboard

setup:
	pip install --upgrade pip
	pip install -r requirements.txt

pipeline:
	python src/db/schema.py
	python src/db/load.py
	python src/analysis/frequencies.py
	python src/analysis/plots.py
	python src/analysis/stats.py
	python src/analysis/subset_analysis.py

dashboard:
	streamlit run src/dashboard/app.py --server.address 0.0.0.0 --server.port 8501
