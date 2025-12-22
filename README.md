
# generate versioned requirements.txt
pip-compile backend/pyproject.toml -o backend/requirements.txt
# optionally dev extras
pip-compile backend/pyproject.toml --extra dev -o backend/requirements-dev.txt
