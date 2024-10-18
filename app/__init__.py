from flask import Flask
from .models.book import book_bp
from .routes.book_routes import books_bp
def create_app():
    app = Flask(__name__)
    app.register_blueprint(book_bp)
    app.register_blueprint(books_bp)
    return app
