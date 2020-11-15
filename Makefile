python = python
ifdef PYTHON
	python = ${PYTHON}
endif

twine = ${python} -m twine
pip = ${python} -m pip

install-local: build-module
	${pip} uninstall -y windowsdnsserver-py
	${pip} install windowsdnsserver-py --no-index --find-links dist/

upload: build-module
	@${twine} upload dist/* -r testpypi

upload-prod: build-module
	@${twine} upload dist/* -r pypi

build-module:
	rm -rf build
	rm -rf dist
	${python} setup.py sdist
	${python} setup.py bdist_wheel