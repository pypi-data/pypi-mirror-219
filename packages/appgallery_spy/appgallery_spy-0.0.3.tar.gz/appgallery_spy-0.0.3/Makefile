install:
	python -m pip install --upgrade pip
	python -m pip install flit
	flit install --deps develop

isort:
	isort ./appgallery_spy ./tests

format: isort
	black .

test:
	pytest --cov=appgallery_spy/ --cov-report=term-missing --cov-fail-under=100

bumpversion-major:
	bumpversion major

bumpversion-minor:
	bumpversion minor

bumpversion-patch:
	bumpversion patch

