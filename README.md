# rosetta-be

# Daniel's Instructions - Edits Needed to Combine Daniel's and Matt's instructions below
## Local Deployment

### Python & Flask Setup

- Install Pyenv with Homebrew
    ```
    brew install pyenv
    ```
- Install Python 3.7.7 with Pyenv
    ```
    pyenv install 3.7.7
    ```
- Install Pip
- Use Pip to install packages in requirements.txt:
    ```
    pip install -r requirements.txt
    ```

### Database Setup

- Install PostgreSQL with Homebrew
    ```
    brew install postgresql
    ```
- Create database from terminal
    - Open interactive PostgreSQL session:
        ```
        psql
        ```
    - Enter SQL command to create empty database:
        ```
        CREATE DATABASE rosetta_dev
        ```
- Run migrations to add tables to database
    ```
    python flaskr/manage.py db upgrade
    ``` 

### Starting Flask

- To run server:
    ```
    flask run
    ```
- To run Flask shell session with access to ORM:
    ```
    python flaskr/manage.py shell
    ```
    
# Matt's Instructions - Edits Needed
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