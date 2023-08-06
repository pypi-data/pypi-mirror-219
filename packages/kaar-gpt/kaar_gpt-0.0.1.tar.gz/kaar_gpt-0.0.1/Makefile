.PHONY: clean build upload

build: clean
	python -m pip install --upgrade build
	python -m build

upload: build
	python -m pip install --upgrade twine
	python -m twine upload dist/* --verbose

clean:
	rm -rf build dist
	rm -rf *.egg-info

