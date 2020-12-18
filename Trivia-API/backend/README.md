# Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3

Follow instructions to install the latest version of Python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is a Python SQL toolkit and an ORM used to handle a lightweight SQLite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is an extension used to handle cross origin requests from the frontend server. 

## Database Setup

With PostgreSQL running, restore a database using the trivia.psql file provided. From the `backend` directory in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

To run the server, execute from within the `backend` directory:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs Flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail: 
- 400: Bad Request
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity

### Endpoints
**GET /questions**
- Fetches a list of all questions, paginated in groups of 10
- Request Arguments: `page` (integer, optional, defaults to 1)
- Returns a list of question objects, the success value, the total number of questions, all categories and the current category.
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
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
  "total_questions": 28
}
```

**GET /categories**
- Fetches a list of all categories
- Request Arguments: None
- Returns a list of category objects, the success value, and the total number of categories.
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```

**GET /categories/{category_id}/questions**
- Fetches a list of questions based on category, paginated in groups of 10
- Request Arguments: 
  - `category_id` (integer, mandatory)
  - `page` (integer, optional, defaults to 1)
- Returns a list of questions based on category, the success value, the total number of questions and the current category.
- Sample: `curl http://127.0.0.1:5000/categories/6/questions`

```
{
  "current_category": "Sports", 
  "questions": [
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
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

**DELETE /questions/{question_id}**
- Deletes the question of the given ID if it exists.
- Request Arguments: `question_id` (integer, mandatory)
- Returns the id of the deleted question, the success value, the total number of questions, and the question list based on the current page number to update the frontend. 
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/36?page=3`

```
{
  "deleted": 36, 
  "questions": [
    {
      "answer": "Heath Ledger", 
      "category": 5, 
      "difficulty": 3, 
      "id": 37, 
      "question": "Who played the Joker character in the Dark Knight movie?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```

**POST /questions**
- Creates a new question using the submitted question and answer text, category, and difficulty score.
- Request Arguments: None
- Returns the id of the created question, the success value, the total number of questions, and the question list based on the current page number to update the frontend.
- Sample: `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"Who played the Joker character in the Dark Knight movie?", "answer":"Heath Ledger", "category":"5", "difficulty":"3"}'`

```
{
  "created": 37, 
  "questions": [
    {
      "answer": "yes", 
      "category": 5, 
      "difficulty": 1, 
      "id": 36, 
      "question": "Was Meryl Streep nominated for the Academy Award for The Devil Wears Prada?"
    }, 
    {
      "answer": "Heath Ledger", 
      "category": 5, 
      "difficulty": 3, 
      "id": 37, 
      "question": "Who played the Joker character in the Dark Knight movie?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```

**POST /questions/search**
- Searches for a question based on a search term.
- Request Arguments: None
- Returns questions that match the search term, the success value and the total number of questions.    
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Tom Hanks"}'`

```
{
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

**POST /quizzes**
- Initiates (or continues) a quiz, returning a question at random based on the selected category (or any category, if "ALL" was selected).
- Request Arguments: None
- Returns a random questions within the given category, if provided (not one of the previous questions) and the success value.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"click","id":0}}'`

```
{
  "question": {
    "answer": "The Palace of Versailles", 
    "category": 3, 
    "difficulty": 3, 
    "id": 14, 
    "question": "In which royal palace would you find the Hall of Mirrors?"
  }, 
  "success": true
}
```

## Testing
To run the tests, execute:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
