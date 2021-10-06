# Project: Data Storage and Preparation
# Author: Jiri Kristof
# Date: 06-10-2021

PYTHON=python
PYTEST=pytest
PIP=pip
REQUIREMENTS=requirements.txt

.PHONY: run test

run:

test:
	cd src & ${PYTEST}

install:
	${PYTHON} -m ${PIP} install ${REQUIREMENTS}
