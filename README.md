# Messages REST API

REST API for managing messages. It supports messages and user resources including authentication (JWT). Working application can be found [here](https://messages-flask-api.herokuapp.com/api/v1/).

The documentation can be found in `api/templates/api_documentation.html` or [here published](https://documenter.getpostman.com/view/13065363/TWDRrePa#fcb01dc2-ca6c-4b9d-ae42-329741a49a3b).
The schema of the database can be found [here](https://dbdiagram.io/d/6025b5b380d742080a3a38c5)

## Setup

- Clone repository
- Create database and user
- Rename .env.example to `.env` and set your values 
```buildoutcfg
# MySQL SQLALCHEMY_DATABASE_URI template
SQLALCHEMY_DATABASE_URI = mysql+pymysql://<db_user>:<db_password>@<db_host>/<db_name>?charset=utf8mb4

# PostgreSQL SQLALCHEMY_DATABASE_URI template
SQLALCHEMY_DATABASE_URI = postgresql+psycopg2://<db_user>:<db_password>@<db_host>/<db_name>
```
- Create a virtual environment
```buildoutcfg
python -m venv venv
```
- Install packages from `requirements.txt`
```buildoutcfg
pip install -r requirements.txt
```
- Migrate database
```buildoutcfg
flask db upgrade
```
- Run command
```buildoutcfg
flask run
```

### NOTE

Import / delete example data from 
`api/samples`
```buildoutcfg
# import examples
flask db-manage add-data

# remove all data
flask db-manage remove-data
```

## Tests

In order to execute tests (with details) located in `tests/` run the command:
```buildoutcfg
python -m pytest -v
```

## Technologies / Tools

- Python 3.7.3
- Flask 1.1.2
- Alembic 1.5.4
- SQL Alchemy 1.3.23
- Pytest 6.2.2
- Marshmallow 3.10.1
- JWT 1.7.1
- PostgreSQL
- Heroku
- Postman
