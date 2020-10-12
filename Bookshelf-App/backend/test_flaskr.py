import json
import os
import unittest

from flaskr import create_app
from models import setup_db, Book

class BookTestCase(unittest.TestCase):
    ''' This class represents the book test case '''

    def setUp(self):
        ''' Define test variables and initialize the app '''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'bookshelf_test'
        self.database_path = 'postgres://{}@{}/{}'.format('monika','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Flight of the Storks',
            'author': 'Jean-Christophe Grange',
            'rating': 4
        }

    def tearDown(self):
        ''' Executed after each test '''
        pass

    def test_get_paginated_books(self):
        response = self.client().get('/books')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_404_sent_requesting_beyond_valid_page(self):
        response = self.client().get('/books?page=1000', json={'rating': 1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_book_with_results(self):
        response = self.client().post('/books', json={'search': 'Mountain'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertEqual(len(data['books']), 4)

    def test_get_book_search_without_results(self):
        response = self.client().post('/books', json={'search': 'applejacks'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_books'], 0)
        self.assertEqual(len(data['books']), 0)

    def test_update_book_rating(self):
        response = self.client().patch('/books/2', json={'rating': 1})
        data = json.loads(response.data)
        book = Book.query.filter(Book.id == 2).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 1)

    def test_400_for_failed_update(self):
        response = self.client().patch('/books/2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_book(self):
        response = self.client().delete('/books/5')
        data = json.loads(response.data)

        book = Book.query.filter(Book.id == 5).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
        self.assertEqual(book, None)

    def test_422_if_book_does_not_exist(self):
        response = self.client().delete('/books/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_create_new_book(self):
        response = self.client().post('/books', json=self.new_book)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['books']))

    def test_405_if_book_creation_not_allowed(self):
        response = self.client().post('/books/45', json=self.new_book)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()