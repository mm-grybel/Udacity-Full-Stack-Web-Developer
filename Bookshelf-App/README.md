# Bookshelf App
This project is a virtual bookshelf. Users can add their books to the bookshelf, rate books, update the ratings and search through their book list. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development
Developers using this project should already have Python 3 and pip installed.

### Backend
From the backend folder run `pip install -r requirements.txt`. All required packages are included in the requirements file.

To run the application locally, run the following commands: <br>
`export FLASK_APP=flaskr` <br>
`export FLASK_ENV=development` <br>
`flask run`

These commands put the application in the development mode and direct the application to use the `__init__.py` file in the `flaskr` folder. Working in the development mode shows an interactive debugger in the console and restarts the server whenever any changes are made.

The application is run on `http://127.0.0.1:5000/` by default.

### Tests
To run tests, navigate to the `backend` folder and run the following command: <br>
`python test_flaskr.py`

All tests are kept in that file and should be maintained as updates are made to the app functionality.

## API Reference

### Getting Started
- Base URL: at present, this app can only run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`
- Authentication: this version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail: 
- 400: Bad Request
- 404: Not Found
- 422: Unprocessable Entity

### Endpoints
**GET /books**
- General:
    - Returns the list of book objects, the success value, and the total number of books
    - Results are paginated in the groups of 8. Include a request argument to choose the page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/books`

```
{
  "books": [
    {
      "author": "Harlan Coben", 
      "id": 1, 
      "rating": 3, 
      "title": "The Woods"
    }, 
    {
      "author": "Jon Krakauer", 
      "id": 2, 
      "rating": 4, 
      "title": "Into Thin Air"
    }, 
    {
      "author": "Ed Viesturs", 
      "id": 3, 
      "rating": 5, 
      "title": "No Shortcuts to the Top"
    }, 
    {
      "author": "Thomas Harris", 
      "id": 4, 
      "rating": 4, 
      "title": "The Silence of the Lambs"
    }, 
    {
      "author": "Robert Birkby", 
      "id": 5, 
      "rating": 4, 
      "title": "Mountain Madness"
    }, 
    {
      "author": "Chris Carter", 
      "id": 6, 
      "rating": 4, 
      "title": "One by One"
    }
  ], 
  "success": true, 
  "total_books": 6
}
```

**POST /books**
- General:
    - Creates a new book using the submitted title, author and rating. Returns the id of the created book, the success value, and the book list based on the current page number to update the frontend.
- Sample: `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"This Is Going to Hurt: Secret Diaries of a Junior Doctor", "author":"Adam Kay", "rating":"5"}'`

```
{
  "books": [
      {
          "author": "Adam Kay",
          "id": 7,
          "rating": 5,
          "title": "This Is Going to Hurt: Secret Diaries of a Junior Doctor"
      }
  ], 
  "created": 7, 
  "success": true, 
  "total_books": 7
}
```

**DELETE /books/{book_id}**
- General:
    - Deletes the book of the given ID if it exists. Returns the id of the deleted book, the success value, the total number of books, and the book list based on the current page number to update the frontend.
- Sample: `curl -X DELETE http://127.0.0.1:5000/books/2?page=1`

```
{
  "books": [
    {
      "author": "Harlan Coben", 
      "id": 1, 
      "rating": 3, 
      "title": "The Woods"
    }, 
    {
      "author": "Ed Viesturs", 
      "id": 3, 
      "rating": 5, 
      "title": "No Shortcuts to the Top"
    }, 
    {
      "author": "Thomas Harris", 
      "id": 4, 
      "rating": 4, 
      "title": "The Silence of the Lambs"
    }, 
    {
      "author": "Robert Birkby", 
      "id": 5, 
      "rating": 4, 
      "title": "Mountain Madness"
    }, 
    {
      "author": "Chris Carter", 
      "id": 6, 
      "rating": 4, 
      "title": "One by One"
    }, 
    {
      "author": "Adam Kay", 
      "id": 7, 
      "rating": 5, 
      "title": "This Is Going to Hurt: Secret Diaries of a Junior Doctor"
    }
  ], 
  "deleted": 2, 
  "success": true, 
  "total_books": 6
}
```

**PATCH /books/{book_id}**
- General:
    - If provided, updates the rating of the specified book. Returns the success value and the id of the modified book.
- Sample: `curl http://127.0.0.1:5000/books/3 -X PATCH -H "Content-Type: application/json" -d '{"rating":"4"}'`

```
{
  "id": 3, 
  "success": true
}
```
