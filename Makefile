init:
	pip install bumpversion pytest pytest-cov

test:
	py.test test_lumpy.py

cov:
	py.test --cov=lumpy --cov-report term-missing --verbose

patch:
	bumpversion patch

minor:
	bumpversion minor

major:
	bumpversion major

release:
	#Examples:
	#  make patch release
	#  make minor release
	#  make major release
	git push origin master
	git push origin `git describe --abbrev=0 --tags`
