# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

It is recommended to work within a virtual environment. This keeps the dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment set up and running, install the dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. **Flask** is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight **SQLite** database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for **JSON Web Tokens** (JWTs). Useful for encoding, decoding, and verifying the JWTs.

## Running the server

From within the `./src` directory, first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect the file changes and restart the server automatically.

## Tasks performed

### Setup Auth0

1. Created a new Auth0 Account.
2. Selected a unique tenant domain.
3. Created a new, single page web application.
4. Created a new API.
    - In API Settings set the following options:
        - `Enable RBAC`
        - `Enable Add Permissions in the Access Token`
5. Created new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Created new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Tested the endpoints with [Postman](https://getpostman.com). 
    - Registered 2 users - assigned the Barista role to one of them and the Manager role to the other.
    - Signed into each account and made a note of the JWT.
    - Imported the Postman collection `./backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for the barista and the manager, navigated to the authorization tab, and included the JWT in the Token field.
    - Ran the collection and corrected any errors.
    - Exported the collection overwriting the initial setup.

### Implement The Server

Completed all `@TODO` sections throughout the `./backend/src`:

1. `./src/auth/auth.py`
2. `./src/api.py`
