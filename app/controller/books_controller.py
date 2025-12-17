from flask import Blueprint, request,render_template,redirect ,url_for
from flask_login import login_required

from app.model.book import BookRepo

bp = Blueprint("books", __name__, url_prefix="/books")

repo = BookRepo()

@bp.get("/")
@login_required
def list_books():
    books = repo.all()
    return render_template("books/list.html", books=books) # отдаём View

@bp.post("/")
def create_book():
    title = request.form.get("title")
    author = request.form.get("author")
    repo.add(title, author)
    return redirect(url_for("books.list_books"))


@bp.post("/delete/<int:book_id>")
def delete_book(book_id):
    repo.delete(book_id)
    return redirect(url_for("books.list_books"))

@bp.post("/update")
def update_book():
    book_id = request.form.get('id')
    title = request.form.get('new_title')
    author = request.form.get('new_author')
    repo.update(book_id, title, author)
    return redirect(url_for("books.list_books"))