# rosetta-be

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
