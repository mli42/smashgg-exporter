# SmashGG Exporter

- [Start the project](#start-the-project)
  * [Create and populate `.env` file](#create-and-populate-env-file)
  * [Install dependencies](#install-dependencies)
      + [Install Python](#install-python)
      + [Install Poetry](#install-poetry)
      + [Install project dependencies with Poetry](#install-project-dependencies-with-poetry)
  * [Run the project](#run-the-project)
  * [Usage](#usage)
- [Misc](#misc)

## Start the project

### Create and populate `.env` file

```bash
cp .env.example .env
```

### Install dependencies

#### Install Python

Python 3.10 or newer is required.

#### Install Poetry

Please follow the steps on their website: https://python-poetry.org/docs/#installation

#### Install project dependencies with Poetry

```bash
poetry install
```

### Run the project

There is two ways to run the project:

<details>
<summary>Via Poetry CLI</summary>

```bash
poetry run python src/main.py
```
</details>

<details>
<summary>Via virtual env</summary>

Activate virtual env (only once per terminal):

```bash
source .venv/bin/activate
```

Then use python directly:

```bash
python src/main.py
```
</details>

### Usage

`main.py`
```
$ python src/main.py --help

usage: main.py [-h] [--startDate STARTDATE] [--endDate ENDDATE] [--countryCode COUNTRYCODE] [--addrState ADDRSTATE]

Fetches sets from start.gg and saves them into a postgres database

options:
  -h, --help            show this help message and exit
  --startDate STARTDATE
                        fetch from startDate DD-MM-YYYY (default: 01-01-2025)
  --endDate ENDDATE     fetch up to endDate DD-MM-YYYY (default: 01-04-2025)
  --countryCode COUNTRYCODE
                        CountryCode of the tournament, can be set to `None` (default: FR)
  --addrState ADDRSTATE
                        AddrState of the tournament, can be set to `None` (default: IDF)
```

`export_db_to_csv.py`
```
$ python src/export_db_to_csv.py --help
usage: export_db_to_csv.py [-h] [--startDate STARTDATE] [--endDate ENDDATE] [--countryCode COUNTRYCODE] [--addrState ADDRSTATE] [--outSuffix OUTSUFFIX]

Fetches sets from database and saves them in a local csv

options:
  -h, --help            show this help message and exit
  --startDate STARTDATE
                        fetch from startDate DD-MM-YYYY (default: 01-01-2025)
  --endDate ENDDATE     fetch up to endDate DD-MM-YYYY (default: 01-04-2025)
  --countryCode COUNTRYCODE
                        CountryCode of the tournament, can be set to `None` (default: FR)
  --addrState ADDRSTATE
                        AddrState of the tournament, can be set to `None` (default: IDF)
  --outSuffix OUTSUFFIX
                        csv output filename to `output/{timestamp}-{outSuffix}.csv` (default: `output/{timestamp}.csv`)
```


## Misc

<details>
<summary>start.gg addrState in France</summary>

- `Auvergne-Rhône-Alpes`
- `Bourgogne-Franche-Comté`
- `Bretagne`
- `Centre-Val de Loire`
- `Grand Est`
- `Hauts-de-France`
- `Île-de-France`, `IDF`
- `Normandie`
- `Nouvelle-Aquitaine`
- `Occitanie`
- `Pays de la Loire`
- `Provence-Alpes-Côte d'Azur`

:warning: `IDF` and `Île-de-France` behave like two different addrState and have to be fetched separately
</details>

<details>
<summary>Poetry</summary>

```bash
# Clear Poetry cache
poetry cache clear --all .

# Delete all virtual environments
poetry env remove --all
```
</details>

<details>
<summary>Alembic</summary>

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
</details>
