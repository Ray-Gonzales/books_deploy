from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.user_model import User
from flask_app.models.book_model import Book

@app.route("/books")
def books():
    return render_template("books.html" , books = Book.get_all())

@app.route("/create/book" , methods = ['POST'])
def create_book():
    data = {
        "title":request.form['title'],
        "num_of_pages": request.form['num_of_pages']
    }
    book_id = Book.save(data)
    return redirect("/books")

@app.route("/book/<int:id>")
def show_book(id):
    data = {
        "id":id
    }
    return render_template("bookshelf.html" , book = Book.get_book_with_users(data) , unfavorited_authors = User.unfavorited_authors(data))

@app.route("/join/author",methods=['POST'])
def join_author():
    data = {
        "user_id": request.form["user_id"],
        "books_id": request.form["books_id"]
    }
    User.add_favorite(data)
    return redirect(f"/book/{request.form['books_id']}")