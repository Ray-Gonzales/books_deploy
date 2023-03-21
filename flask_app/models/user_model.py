from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book_model

class User:
    db = "books"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( name, created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_user_with_books(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON users.id = favorites.user_id LEFT JOIN books ON books.id = favorites.books_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        user = cls(results[0])
        for row_from_db in results:
            if row_from_db["books.id"] == None:
                break
            book_data = {
                "id" : row_from_db["books.id"],
                "title" : row_from_db["title"],
                "num_of_pages" : row_from_db["num_of_pages"],
                "created_at" : row_from_db["books.created_at"],
                "updated_at" : row_from_db["books.updated_at"],
            }
            user.favorite_books.append( book_model.Book( book_data) )
        return user

    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM users WHERE users.id NOT IN ( SELECT user_id FROM favorites WHERE books_id = %(id)s );"
        users = []
        results = connectToMySQL(cls.db).query_db(query,data)
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (user_id,books_id) VALUES (%(user_id)s,%(books_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)