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

## Filters

- [x] Location: 48.853495,2.348391 (Paris, France)
- [x] Location radius: 5mi
- [x] Location: FR, IDF
- [x] After: 1735689600 (1 January 2025 00:00:00)
- [x] Before: 1743465600 (1 April 2025 00:00:00)
- [x] Video Game: SSBU
- [ ] Filter out events "Listes d'attentes", ladders(?)

## Misc

### Clear Poetry cache

```bash
poetry cache clear --all .
```

### Delete all virtual environments

```bash
poetry env remove --all
```
