# rosetta-be

## Local Deployment

### Python & Flask Setup

- Install Pyenv with Homebrew
    ```
    brew install pyenv
    ```
- Add pyenv init to your shell profile (see instructions [here under step 3](https://github.com/pyenv/pyenv#basic-github-checkout))
    - If using Bash, enter the following in your terminal:
        ```
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
        ```
    - If using Zsh, use the following:
        ```
        echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
        ```
- Restart terminal to allow changes to take effect.
- Install Python 3.7.7 with Pyenv
    ```
    pyenv install 3.7.7
    ```
- Set up virtual environment
    ```
    python3 -m venv venv
    . venv/bin/activate
    ```
- Upgrade Pip (or, if not made available by Python 3, [install Pip](https://pip.pypa.io/en/stable/installing/#))
    ```
    pip install -U pip
    ```
- Use Pip to install packages in requirements.txt:
    ```
    pip install -r requirements.txt
    ```
- Set environment variables:
    ```
    export FLASK_APP=flaskr/app
    export FLASK_ENV=development
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
        CREATE DATABASE rosetta_dev;
        ```
- Run migrations to add tables to database

    ```
    python flaskr/manage.py db upgrade
    ```
    - If you had to drop your DB in development, you will need to run `python flaskr/manage.py db migrate` before `python flaskr/manage.py db upgrade`

- If you need to populate your database, run the following commands, but if possible, it's preferable to import this from an already populated database, such as the Rosetta production server database (to be added):
   ```
   python flaskr/manage.py get_ruby_methods
   python flaskr/manage.py get_js_methods
   ```

### Starting Flask

- To run server on `localhost:5000`:
    ```
    flask run
    ```
- To run Flask shell session with access to ORM:
    ```
    python flaskr/manage.py shell
    ```

### Accessing GraphQL Endpoint
(This is intended for current developers and will be edited before final docs are published)
- Locally: `localhost:5000/graphql`
   - This will bring up the GraphiQL interface
   - To get all languages:
   ```
   {
     allLanguages{
       edges{
         node{
           name
           id
           }
         }
       }
     }
  ```
  - To get all methods:
  ```
  {
    allMethods{
      edges{
        node{
          name
          }
        }
      }
    }
  ```
  - To get all methods with language node:
  ```
  {
    allMethods{
      edges{
        node{
          name
          snippet
          language {
            name
          }
        }
      }
    }
  }
  ```
  - To get the first 5 methods of the 1st language:
  ```
  {
    allLanguages(first:1){
      edges{
        node{
          name
          methods(first:5) {
            edges {
              node {
                name
                description
              }
            }
          }
        }
      }
    }
  }
  ```
  Example Response:
  ```js
  {
    "data": {
      "allLanguages": {
        "edges": [
          {
            "node": {
              "name": "Ruby",
              "methods": {
                "edges": [
                  {
                    "node": {
                      "name": "method-i-26",
                      "description": "Set Intersection — Returns a new array containing unique elements common to\nthe two arrays. The order is preserved from the original array.\nIt compares elements using their hash and eql? methods for efficiency.\nSee also #uniq.\n"
                    }
                  },
                  {
                    "node": {
                      "name": "method-i-2A",
                      "description": "Repetition — With a String argument, equivalent\nto ary.join(str).\nOtherwise, returns a new array built by concatenating the int\ncopies of self.\n"
                    }
                  },
                  {
                    "node": {
                      "name": "method-i-2B",
                      "description": "Concatenation — Returns a new array built by concatenating the two arrays\ntogether to produce a third array.\nNote that\nis the same as\nThis means that it produces a new array. As a consequence, repeated use of\n+= on arrays can be quite inefficient.\nSee also #concat.\n"
                    }
                  },
                  {
                    "node": {
                      "name": "method-i-2D",
                      "description": "Array Difference\nReturns a new array that is a copy of the original array, removing any\nitems that also appear in other_ary. The order is preserved\nfrom the original array.\nIt compares elements using their hash and eql? methods for efficiency.\nIf you need set-like behavior, see the library class Set.\nSee also #difference.\n"
                    }
                  },
                  {
                    "node": {
                      "name": "method-i-3C-3C",
                      "description": "Append—Pushes the given object on to the end of this array. This expression\nreturns the array itself, so several appends may be chained together.\n"
                    }
                  }
                ]
              }
            }
          }
        ]
      }
    }
  }
  ```
