.PHONY: today list

objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

setup:
	@pip install -r requirements.txt --no-cache-dir
	@echo 'Installed all requirements to (virtual) environment'

test_suite:
	@pytest test/
	@echo 'Running tests'

run_dev:
	@uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info

run:
	@uvicorn main:app --host 0.0.0.0 --port 8000

today:
	@date

list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null \
	| awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
	| sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

