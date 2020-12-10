all: venv
	@git submodule foreach git pull origin main
	@git pull
	./venv/bin/python scripts/process.py
	@git diff data

venv: scripts/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur scripts/requirements.txt
	touch venv

clean:
	rm -rf data/*.csv
	rm -rf pdfs/*.pdf

.PHONY: clean
