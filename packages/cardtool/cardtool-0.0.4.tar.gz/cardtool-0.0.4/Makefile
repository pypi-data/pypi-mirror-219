init:
	pip install -r ./requirements.txt

freeze:
	pip freeze > ./requirements.txt

lint:
	autoflake -i -r src/ tests/
	isort src/ tests/
	black src/ tests/
	flake8 src/ tests/

test-cov:
	pytest --cov --cov-append --cov-report=term-missing

test-unit:
	pytest

coverage:
	coverage erase
	pytest --cov --cov-append --cov-report=term-missing
	tox -e report
	open htmlcov/index.html

pre-commit-install:
	pre-commit install

validate:
	tox

submit-coverage:
	curl https://keybase.io/codecovsecurity/pgp_keys.asc | gpg --no-default-keyring --keyring trustedkeys.gpg --import
	curl -Os https://uploader.codecov.io/latest/linux/codecov
	curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM
	curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM.sig
	gpgv codecov.SHA256SUM.sig codecov.SHA256SUM
	shasum -a 256 -c codecov.SHA256SUM
	chmod +x codecov
	./codecov