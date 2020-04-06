# rosetta-be
## Local Setup Instructions

1. Set up virtual environment:
```
$ python3 -m venv venv
$ . venv/bin/activate
```
2. Install dependencies:
`$ pip install -r requirements.txt`

3. Set environment variables:
```
$ export FLASK_APP=flaskr/app
$ export FLASK_ENV=development
```
4. Migrate database:
```
$ python flaskr/manage.py db init
$ python flaskr/manage.py db migrate
$ python flaskr/manage.py db upgrade
```
5. Boot local server:
`$ flask run`
The local server runs on port 5000.
