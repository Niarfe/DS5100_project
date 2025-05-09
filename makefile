default:
	@cat makefile

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt

test:
	clear
	pytest -v tests/test_montecarlo.py

lint:
	pylint montecarlo
