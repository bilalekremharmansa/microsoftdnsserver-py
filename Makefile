python = python
ifdef PYTHON
	python = ${PYTHON}
endif

twine = ${python} -m twine
pip = ${python} -m pip

upload: build
	@${twine} upload dist/* -r testpypi

build:
	rm -rf build
	rm -rf dist
	${python} setup.py sdist
	${python} setup.py bdist_wheel
