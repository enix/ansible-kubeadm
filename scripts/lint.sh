
set -e

poetry install --only=lint
#if ! poetry run sh -c "command -v ansible-lint --version > /dev/null"; then
#    poetry run pip install ansible-lint==6.14.3
#fi

poetry run yamllint .
poetry run isort --check .
poetry run black --check .
poetry run flake8 .
#poetry run ansible-lint
