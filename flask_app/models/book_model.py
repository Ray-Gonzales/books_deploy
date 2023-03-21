from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
import pprint

class Book:
    db = "books"
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.users_favorite = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO books ( title , num_of_pages , created_at , updated_at ) VALUES ( %(title)s , %(num_of_pages)s , NOW() , NOW() );"
        return connectToMySQL(cls.db).query_db( query, data )
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.db).query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
        return books
    
    @classmethod
    def get_book_with_users(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.books_id = books.id LEFT JOIN users ON favorites.user_id = users.id WHERE books.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print("------------------------------------------------------------------------")
        pprint.pprint(results, sort_dicts=False)
        book = cls(results[0])
        for row_from_db in results:
            if row_from_db["users.id"] == None:
                break
            user_data = {
                "id" : row_from_db["users.id"],
                "name" : row_from_db["name"],
                "created_at" : row_from_db["users.created_at"],
                "updated_at" : row_from_db["users.updated_at"],
            }
            book.users_favorite.append( user_model.User( user_data) )
        return book
    
    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT books_id FROM favorites WHERE user_id = %(id)s );"
        results = connectToMySQL(cls.db).query_db(query,data)
        books = []
        for book in results:
            books.append(cls(book))
        print(books)
        return books