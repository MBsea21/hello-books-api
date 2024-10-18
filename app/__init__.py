from flask import Flask
from .models.book import book_bp
def create_app():
    app = Flask(__name__)
    app.register_blueprint(book_bp)
    return app
