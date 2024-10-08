PIP := dummyenv/bin/pip
PYTHON := dummyenv/bin/python3


clear:
	rm -rf dummyenv

venv:
	python3 -m venv dummyenv

reqs:
	${PIP} install -r requirements.txt

run:
	${PYTHON} runner.py

freeze:
	${PIP} freeze > requirements.txt


launch:
	make clear
	make venv
	make reqs
	make run
