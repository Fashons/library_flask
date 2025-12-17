from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


class BookRepo:
    def all(self):
        return Book.query.all()  # ← Используем Book.query — он сам найдёт сессию

    def add(self, title, author):
        book = Book(title=title, author=author)
        db.session.add(book)
        db.session.commit()
        return book

    def delete(self, book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return book

    def update(self, book_id, title, author):
        book = Book.query.get(book_id)
        book.title = title
        book.author = author
        db.session.commit()
        return book