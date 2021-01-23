demo:
	env cat doc/demo && env cat
.PHONY: demo

publish:
	rm -f dist/*
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
.PHONY: publish
