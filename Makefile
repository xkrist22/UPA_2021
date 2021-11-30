# Project: Data Storage and Preparation
# Author: Jiri Kristof
# Date: 06-10-2021

PYTHON=python
PYTEST=pytest
PIP=pip
REQUIREMENTS=requirements.txt

.PHONY: run test

run1:
	${PYTHON} proj1.py

run2:
	${PYTHON} proj2.py

test:
	cd src & ${PYTEST}

install:
	${PYTHON} -m ${PIP} install ${REQUIREMENTS}
