.PHONY: autoformat tests

autoformat:
	git ls-files | grep -P '\.py$$' | xargs isort
	git ls-files | grep -P '\.py$$' | xargs black -S

tests:
	pytest
	git ls-files | grep -P '\.py$$' | xargs black -S --check
	git ls-files | grep -P '\.py$$' | xargs flake8 --select F821,F401
