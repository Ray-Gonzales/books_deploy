from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.user_model import User
from flask_app.models.book_model import Book

@app.route("/")
def index():
    return redirect("/authors")

@app.route("/authors")
def authors():
    return render_template("authors.html" , users = User.get_all() )

@app.route("/create/author" , methods = ['POST'])
def create_author():
    data = {
        "name": request.form['name']
    }
    user_id = User.save(data)
    return redirect("/authors")

@app.route("/author/<int:id>")
def show_author(id):
    data = {
        "id": id
    }
    return render_template("show_author.html" , user = User.get_user_with_books(data) , unfavorited_books = Book.unfavorited_books(data))

@app.route("/join/book",methods=['POST'])
def join_book():
    data = {
        "user_id": request.form['user_id'],
        "books_id": request.form['books_id']
    }
    User.add_favorite(data)
    return redirect(f"/author/{request.form['user_id']}")
