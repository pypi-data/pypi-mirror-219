
.PHONY: clean build upload

build: clean
	python -m pip install --upgrade build
	python -m build

upload: build
	python -m pip install --upgrade twine
	python -m twine upload dist/* --verbose

pipx-uninstall:
	pipx uninstall kaar-gpt-tools
.PHONY: pipx-uninstall

pipx-install:
	pipx install dist/*.whl
.PHONY: pipx-install

clean:
	rm -rf build dist
	rm -rf *.egg-info
