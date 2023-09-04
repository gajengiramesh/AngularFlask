SQLite:
    loading the existing database / creating new database and load it from the script
    cmd
    C:\Working\dev\sqlite\sqlite3.exe C:\Working\dev\Python\FlaskResterExample\test.db
    .read C:\Working\dev\Python\FlaskResterExample\test_dbscript.sql

    creating sql dump from the db
    .dump C:\Working\dev\Python\FlaskResterExample\test_dbscript.sql

Packages installed :
    pip install SQLAlchemy==1.4.49
    pip install Flask==2.3.1
    pip install marshmallow==3.18.0
    pip install coverage
    pip install Flask-JWT-Extended


Running the programme
    C:\Working\dev\Python\FlaskResterExample\run.py

unittests:
    links :
    https://www.pythontutorial.net/python-unit-testing/python-unittest/

    commands:
    python -m unittest tests.services.auth
    python -m unittest tests.services.auth.TestAuthenticator
    python -m unittest tests.services.auth.TestAuthenticator.test_authenticate_notexists
    python -m unittest tests.services.auth -v

coverage :
    https://pypi.org/project/coverage/
    pip install coverage

    links:
    https://www.pythontutorial.net/python-unit-testing/python-unittest-coverage/

    commands:
    python -m coverage run -m unittest tests.services.auth
    python -m coverage report
    python -m coverage html

