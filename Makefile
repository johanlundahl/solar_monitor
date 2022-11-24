
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(dir $(MKFILE_PATH))


init:
	python3 -m pip install -r requirements.txt
	chmod +x solar_monitor/app.py

run:
	python3 -m solar_monitor.app

test:
	coverage run --source=. -m pytest tests/*_test.py

cov:
	coverage report
	coverage html

lint:
	flake8 --statistics --count

update:
	git pull
	sudo pip3 install -r requirements.txt
