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
    - If you encounter the error "Target database is not up to date," you are likely out of sync with the migrations. Run `python flaskr/manage.py db stamp head` to set the current state of your database as "head," then re-attempt to run `db upgrade`.
    - If you had to drop your DB in development, you might need to run `python flaskr/manage.py db migrate` before `python flaskr/manage.py db upgrade`.

- If you need to populate your database, read the instructions below, but if possible, it's preferable to import this from an already populated database, such as the Rosetta production server database (to be added):

NOTE: en_core_web_lg doesn't exist as a package in its own right on pypi.org or Anaconda, so you can't just pip install it by name. Instead, you must run the following command:

`python -m spacy download en_core_web_lg`

Afterwards, run the following scripts to populate the database:

   ```
   python flaskr/manage.py get_ruby_array_methods
   python flaskr/manage.py get_js_array_methods
   python flaskr/relevancy_rating_generator.py
   ```
### Clean the database
If you need to clear your database, run the following commands:

- Enter the psql console: `psql`
- Connect with Rosetta database: `\c rosetta_dev`
- Clear tables: `TRUNCATE TABLE [table_name] RESTART IDENTITY CASCADE;`  

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
   - To get top 5 results in target language as compared to a given method:
   ```
   { translations(targetLanguageId: 2, methodId: 54) {
    	weightedRelevancyRating
    	method {
    	  id
        name
        description
        syntax
        snippet
        docsUrl
    	}
  	}
  }
   ```
   Example response:
   ```js
   {
    "data": {
      "translations": [
        {
          "weightedRelevancyRating": 0.987538288834886,
          "method": {
            "id": "125",
            "name": "Array.prototype.join()",
            "description": "The join() method creates and returns a new string by concatenating all of the elements in an array (or an array-like object), separated by commas or a specified separator string. If the array has only one item, then that item will be returned without using the separator.",
            "syntax": "arr.join([separator])",
            "snippet": "const elements = ['Fire', 'Air', 'Water'];\n\nconsole.log(elements.join());\n// expected output: \"Fire,Air,Water\"\n\nconsole.log(elements.join(''));\n// expected output: \"FireAirWater\"\n\nconsole.log(elements.join('-'));\n// expected output: \"Fire-Air-Water\"\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join"
          }
        },
        {
          "weightedRelevancyRating": 0.836293728101979,
          "method": {
            "id": "139",
            "name": "Array.prototype.toLocaleString()",
            "description": "The toLocaleString() method returns a string representing the elements of the array. The elements are converted to Strings using their toLocaleString methods and these Strings are separated by a locale-specific String (such as a comma “,”).",
            "syntax": "arr.toLocaleString([locales[, options]]);\n",
            "snippet": "const array1 = [1, 'a', new Date('21 Dec 1997 14:12:00 UTC')];\nconst localeString = array1.toLocaleString('en', {timeZone: \"UTC\"});\n\nconsole.log(localeString);\n// expected output: \"1,a,12/21/1997, 2:12:00 PM\",\n// This assumes \"en\" locale and UTC timezone - your results may vary\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toLocaleString"
          }
        },
        {
          "weightedRelevancyRating": 0.823389635377448,
          "method": {
            "id": "116",
            "name": "Array.prototype.fill()",
            "description": "The fill() method changes all elements in an array to a static value, from a start index (default 0) to an end index (default array.length). It returns the modified array.",
            "syntax": "arr.fill(value[, start[, end]])\n",
            "snippet": "const array1 = [1, 2, 3, 4];\n\n// fill with 0 from position 2 until position 4\nconsole.log(array1.fill(0, 2, 4));\n// expected output: [1, 2, 0, 0]\n\n// fill with 5 from position 1\nconsole.log(array1.fill(5, 1));\n// expected output: [1, 5, 5, 5]\n\nconsole.log(array1.fill(6));\n// expected output: [6, 6, 6, 6]\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fill"
          }
        },
        {
          "weightedRelevancyRating": 0.822077852943098,
          "method": {
            "id": "111",
            "name": "Array.of()",
            "description": "The Array.of() method creates a new Array instance from a variable number of arguments, regardless of number or type of the arguments.",
            "syntax": "Array.of(element0[, element1[, ...[, elementN]]])",
            "snippet": "Array.of(7);       // [7] \nArray.of(1, 2, 3); // [1, 2, 3]\n\nArray(7);          // array of 7 empty slots\nArray(1, 2, 3);    // [1, 2, 3]\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/of"
          }
        },
        {
          "weightedRelevancyRating": 0.816790358470725,
          "method": {
            "id": "109",
            "name": "Array.from()",
            "description": "The Array.from() method creates a new, shallow-copied Array instance from an array-like or iterable object.",
            "syntax": "Array.from(arrayLike [, mapFn [, thisArg]])\n",
            "snippet": "console.log(Array.from('foo'));\n// expected output: Array [\"f\", \"o\", \"o\"]\n\nconsole.log(Array.from([1, 2, 3], x => x + x));\n// expected output: Array [2, 4, 6]\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from"
          }
        }
      ]
    }
  }
  ```
   - To get all languages:
   ```
   {
    allLanguages {
      id
      name
      methods {
  			id
        name
      }
    }
  }
  ```
  Example output (partial):
  ```js
  {
  "data": {
    "allLanguages": [
      {
        "id": "1",
        "name": "Ruby",
        "methods": [
          {
            "id": "1",
            "name": "Array::[]"
          },
          {
            "id": "2",
            "name": "Array::new"
          },
          {
            "id": "3",
            "name": "Array::try_convert"
          },
          {
            "id": "4",
            "name": "Array#&"
          },
          {
            "id": "5",
            "name": "Array#*"
          },
          // ...
        ]
      },
      {
        "id": "2",
        "name": "JavaScript",
        "methods": [
          {
            "id": "109",
            "name": "Array.from()"
          },
          {
            "id": "110",
            "name": "Array.isArray()"
          },
          {
            "id": "111",
            "name": "Array.of()"
          },
          {
            "id": "112",
            "name": "Array.prototype.concat()"
          },
          {
            "id": "113",
            "name": "Array.prototype.copyWithin()"
          },
          // ...
        ]
      }
    ]
  }
}
```
