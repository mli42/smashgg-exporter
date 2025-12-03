# SmashGG Exporter

## Start the project

### Create and populate `.env` file

```bash
cp .env.example .env
```

### Install dependencies

#### Install Python

Python 3.10 or newer is required.

#### Install Poetry

> Poetry is a tool for dependency management and packaging in Python.

Please follow the steps on their website: \
https://python-poetry.org/docs/#installation

#### Install project dependencies with Poetry

```bash
poetry install
```

### Run the project

There is two ways to run the project:

#### Via Poetry CLI

```bash
poetry run python src/main.py
```

#### Via virtual env

##### Activate virtual env

To do only once per terminal session:

```bash
source .venv/bin/activate
```

##### Use python directly

```bash
python src/main.py
```

## Misc

### Poetry

```bash
# Clear Poetry cache
poetry cache clear --all .

# Delete all virtual environments
poetry env remove --all
```

### Alembic

```bash
# Get information
alembic current/history

# Create a new migration
alembic revision --autogenerate -m "message"

# Apply migration
alembic upgrade head

# Downgrade migration
alembic downgrade -1
```
