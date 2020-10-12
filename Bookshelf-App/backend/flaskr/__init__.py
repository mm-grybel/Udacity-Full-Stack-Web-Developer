import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    books = [book.format() for book in selection]
    current_books = books[start:end]
    return current_books

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    # A route that retrivies all books, paginated 
    # Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route('/books')
    def retrieve_books():
        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)

        if len(current_books) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'books': current_books,
            'total_books': len(Book.query.all())
        })

    # A route that will update a single book's rating
    # Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):
        body = request.get_json()

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            if 'rating' in body:
                book.rating = int(body.get('rating'))
            book.update()

            return jsonify({
                'success': True,
                'id': book.id
            })
        except:
            abort(400)
    
    # A route that will delete a single book
    # Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    # Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            book.delete()
            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': current_books,
                'total_books': len(Book.query.all())
            })
        except:
            abort(422)

    # A route that create a new book
    # Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to create a new book using the form. 
    # Try doing so from the last page of books. Your new book should show up immediately after you submit it at the end of the page.
    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()

        new_title = body.get('title', None)
        new_author = body.get('author', None)
        new_rating = body.get('rating', None)
        search = body.get('search', None)

        try:
            if search:
                selection = Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search)))
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'books': current_books,
                    'total_books': len(selection.all())
                })
            else:
                book = Book(title=new_title, author=new_author, rating=new_rating)
                book.insert()
                selection = Book.query.order_by(Book.id).all()
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'created': book.id,
                    'books': current_books,
                    'total_books': len(Book.query.all())
                })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': True,
            'error': 405,
            'message': 'method not allowed'
        }), 405
    
    
    return app