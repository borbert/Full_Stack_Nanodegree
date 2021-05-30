# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

Tasks completed in this project

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoint Documentation

### Endpoints
```
GET '/categories'
GET '/questions'
GET '/categories/<category_id>/questions'
POST '/quizzes'
POST '/questions'
POST '/questions/search'
DELETE '/questions/<question_id>'
```
*  GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id:
    - category_string key:value pairs.  
        ``` 
        {'1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"}
        ```
- Example: 
    > curl http://localhost:5000/categories -H "Content-Type: application/json"
    ```
    {
    "categories": [
        {
        "id": 1, 
        "type": "Science"
        }, 
        {
        "id": 2, 
        "type": "Art"
        }, 
        {
        "id": 3, 
        "type": "Geography"
        }, 
        {
        "id": 4, 
        "type": "History"
        }, 
        {
        "id": 5, 
        "type": "Entertainment"
        }, 
        {
        "id": 6, 
        "type": "Sports"
        }
    ], 
    "success": true, 
    "total_categories": 6
    }
    ```

GET '/questions'
- Fetches all questions from the the database
- Request Arguments: None
- Returns: A list of questions, a list of the categories in the trivia database, and a count of the total number of questions.
- Known Errors:
    - 404 status code if no questions are found
- Example:
    > curl http://localhost:5000/questions -H "Content-Type: application/json"
    ```
    {
    "categories": [
        {
        "id": 1, 
        "type": "Science"
        }, 
        {
        "id": 2, 
        "type": "Art"
        }, 
        {
        "id": 3, 
        "type": "Geography"
        }, 
        {
        "id": 4, 
        "type": "History"
        }, 
        {
        "id": 5, 
        "type": "Entertainment"
        }, 
        {
        "id": 6, 
        "type": "Sports"
        }
    ], 
    "questions": [
        {
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }, 
        {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }, 
        {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }, 
        {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
        }, 
        {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
        }, 
        {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
        }, 
        {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
        }, 
        {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
        }, 
        {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ], 
    "success": true, 
    "total_questions": 19
    }

    ```
GET '/categories/<int: category_id>/questions'
- Fetches all questions within a specifc category
- Request Arguments: Category id <category_id>
- Returns: A list of questions within a particular category. 
- Known Errors: 
    - 404 status code id category_id is null
- Example: 
    > curl http://localhost:5000/categories/2/questions -H "Content-Type: application/json"
    ```
    {
    "current_category": "Art", 
    "questions": [
        {
        "answer": "Escher", 
        "category": 2, 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        }, 
        {
        "answer": "Mona Lisa", 
        "category": 2, 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
        }, 
        {
        "answer": "One", 
        "category": 2, 
        "difficulty": 4, 
        "id": 18, 
        "question": "How many paintings did Van Gogh sell in his lifetime?"
        }, 
        {
        "answer": "Jackson Pollock", 
        "category": 2, 
        "difficulty": 2, 
        "id": 19, 
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ], 
    "success": true, 
    "total_questions": 4
    }
    ```
GET '/quizzes'
- Fetches the information needed to start a new quiz
- Request Arguments: None
- Returns:  A randomly selected next question within the same category as the previous question
- Known Errors:
    - 400 status code if the request body is null
    - 400 status code if previous question, quize category, or id are null
- Example:
    > curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"id": 0}}'
    ```
    {
    "question": {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
    }, 
    "success": true
    }
    ```
    > curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [23], "quiz_category": {"type": "Science", "id": 1}}'
    ```
    {
    "question": {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
    }, 
    "success": true
    }
    ```

POST '/questions'
- Creates a new question for trivia app
- Request Arguments:  question, answer, category, difficulty
- Returns:  "Success" to confirm quesiton was added to database and status code 201 
- Known Errors:
    * 400 status code if request_body is empty
    * 405 status code if previous questions are null
    * 400 status code if diffulty is out of the difficulty bounds (1 to 6)
    * 422 status code is question or answer is null
- Example: 
    > curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{ "question": "What is the application used to build great python backends?", "answer": "Flask", "difficulty": 2, "category": 1}'
    ```
    {
    "success": true
    }
    ```
POST '/questions/search'
- Fetches qeustion(s) based upon a supplied search term
- Request Arguments:  search_term which can be a substring of the item being searched for
- Returns:  Status code 200, a list of the questions that contain the substring <search_term>, count of the total questions found, and the search term that was provided.
- Known Errors:
    * 400 status code if the request body or search term are null
    * 404 status code if no questions are retrived
- Example: 
    > curl -X POST http://localhost:5000/questions/search -H "Content-Type: application/json" -d '{"search_term": "title"}'
    ```
    {
    "questions": [
        {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ], 
    "search_term": "title", 
    "success": true, 
    "total_questions": 2
    }
    ```

DELETE '/questions/<question_id>'
- Deletes a question from the database
- Request Arguments: The question id <question_id> to be deleted
- Returns: 'Success' and the question_id deleted
- Known Errors:
        * 404 status code if the question to be deleted is not found in the database
- Example: 
    > curl -X DELETE http://localhost:5000/questions/20 -H "Content-Type: application/json"
    ```
    {
    "deleted": "20", 
    "success": true
    }
    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```