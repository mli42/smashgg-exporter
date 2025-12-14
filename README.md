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

Activate virtual env (only once per terminal):

```bash
source .venv/bin/activate
```

Then use python directly:

```bash
python src/main.py
```

### Usage

```
$ python src/main.py --help

usage: main.py [-h] [--startDate STARTDATE] [--endDate ENDDATE]

Fetches sets from start.gg and saves them into a postgres database

options:
  -h, --help            show this help message and exit
  --startDate STARTDATE
                        fetch from startDate DD/MM/YYYY (default: 01/01/2025)
  --endDate ENDDATE     fetch up to endDate DD/MM/YYYY (default: 01/04/2025)
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
