Default: enviroment

VENV          = .venv
VENV_PYTHON   = .venv/bin/python

#this was ripped off ivs_project_2 project 
.ONESHELL: enviroment
.PHONY: enviroment
$(VENV_PYTHON):
	python3 -m venv ../.venv

enviroment: $(VENV_PYTHON)
	. ../$(VENV)/bin/activate
	pip3 install -r requirements.txt

venv: $(VENV_PYTHON)
	. ../$(VENV)/bin/activate
.PHONY: clean
clean: 
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -fr ../.venv