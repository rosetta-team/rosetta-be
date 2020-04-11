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
   { translations(targetLanguageId: 2, methodId: 58)
     {
       	relevanceRating
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
          "relevanceRating": 0.954340557334369,
          "method": {
            "id": "TWV0aG9kT2JqZWN0OjEyNw==",
            "name": "Array.prototype.lastIndexOf()",
            "description": "The lastIndexOf() method returns the last index at which a given element can be found in the array, or -1 if it is not present. The array is searched backwards, starting at fromIndex.",
            "syntax": "arr.lastIndexOf(searchElement[, fromIndex])\n",
            "snippet": "const animals = ['Dodo', 'Tiger', 'Penguin', 'Dodo'];\n\nconsole.log(animals.lastIndexOf('Dodo'));\n// expected output: 3\n\nconsole.log(animals.lastIndexOf('Tiger'));\n// expected output: 1\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/lastIndexOf"
          }
        },
        {
          "relevanceRating": 0.950875159008615,
          "method": {
            "id": "TWV0aG9kT2JqZWN0OjEyNQ==",
            "name": "Array.prototype.join()",
            "description": "The join() method creates and returns a new string by concatenating all of the elements in an array (or an array-like object), separated by commas or a specified separator string. If the array has only one item, then that item will be returned without using the separator.",
            "syntax": "arr.join([separator])",
            "snippet": "const elements = ['Fire', 'Air', 'Water'];\n\nconsole.log(elements.join());\n// expected output: \"Fire,Air,Water\"\n\nconsole.log(elements.join(''));\n// expected output: \"FireAirWater\"\n\nconsole.log(elements.join('-'));\n// expected output: \"Fire-Air-Water\"\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join"
          }
        },
        {
          "relevanceRating": 0.949436453395991,
          "method": {
            "id": "TWV0aG9kT2JqZWN0OjEyNA==",
            "name": "Array.prototype.indexOf()",
            "description": "The indexOf() method returns the first index at which a given element can be found in the array, or -1 if it is not present.",
            "syntax": "arr.indexOf(searchElement[, fromIndex])",
            "snippet": "const beasts = ['ant', 'bison', 'camel', 'duck', 'bison'];\n\nconsole.log(beasts.indexOf('bison'));\n// expected output: 1\n\n// start from index 2\nconsole.log(beasts.indexOf('bison', 2));\n// expected output: 4\n\nconsole.log(beasts.indexOf('giraffe'));\n// expected output: -1\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf"
          }
        },
        {
          "relevanceRating": 0.948614270616461,
          "method": {
            "id": "TWV0aG9kT2JqZWN0OjEzNQ==",
            "name": "Array.prototype.slice()",
            "description": "The slice() method returns a shallow copy of a portion of an array into a new array object selected from begin to end (end not included) where begin and end represent the index of items in that array. The original array will not be modified.",
            "syntax": "arr.slice([begin[, end]])\n",
            "snippet": "const animals = ['ant', 'bison', 'camel', 'duck', 'elephant'];\n\nconsole.log(animals.slice(2));\n// expected output: Array [\"camel\", \"duck\", \"elephant\"]\n\nconsole.log(animals.slice(2, 4));\n// expected output: Array [\"camel\", \"duck\"]\n\nconsole.log(animals.slice(1, 5));\n// expected output: Array [\"bison\", \"camel\", \"duck\", \"elephant\"]\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice"
          }
        },
        {
          "relevanceRating": 0.944798515639636,
          "method": {
            "id": "TWV0aG9kT2JqZWN0OjExOQ==",
            "name": "Array.prototype.findIndex()",
            "description": "The findIndex() method returns the index of the first element in the array that satisfies the provided testing function. Otherwise, it returns -1, indicating that no element passed the test.",
            "syntax": "arr.findIndex(callback( element[, index[, array]] )[, thisArg])\n",
            "snippet": "const array1 = [5, 12, 8, 130, 44];\n\nconst isLargeNumber = (element) => element > 13;\n\nconsole.log(array1.findIndex(isLargeNumber));\n// expected output: 3\n",
            "docsUrl": "https://developer.mozilla.org//en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/findIndex"
          }
        }
      ]
    }
  }
  ```
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
                      "name": "Array::[]",
                      "description": "Returns a new array populated with the given objects.\n"
                    }
                  },
                  {
                    "node": {
                      "name": "Array::new",
                      "description": "Returns a new array.\nIn the first form, if no arguments are sent, the new array will be empty.\nWhen a size and an optional default are sent, an\narray is created with size copies of default. \nTake notice that all elements will reference the same object\ndefault.\nThe second form creates a copy of the array passed as a parameter (the\narray is generated by calling #to_ary on the parameter).\nIn the last form, an array of the given size is created.  Each element in\nthis array is created by passing the element's index to the given block\nand storing the return value.\nWhen sending the second parameter, the same object will be used as the\nvalue for all the array elements:\nSince all the Array elements store the same hash,\nchanges to one of them will affect them all.\nIf multiple copies are what you want, you should use the block version\nwhich uses the result of that block each time an element of the array needs\nto be initialized:\n"
                    }
                  },
                  {
                    "node": {
                      "name": "Array::try_convert",
                      "description": "Tries to convert obj into an array, using to_ary\nmethod.  Returns the converted array or nil if\nobj cannot be converted for any reason. This method can be\nused to check if an argument is an array.\n"
                    }
                  },
                  {
                    "node": {
                      "name": "Array#&",
                      "description": "Set Intersection — Returns a new array containing unique elements common to\nthe two arrays. The order is preserved from the original array.\nIt compares elements using their hash and eql? methods for efficiency.\nSee also #uniq.\n"
                    }
                  },
                  {
                    "node": {
                      "name": "Array#*",
                      "description": "Repetition — With a String argument, equivalent\nto ary.join(str).\nOtherwise, returns a new array built by concatenating the int\ncopies of self.\n"
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
