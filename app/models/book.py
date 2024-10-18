from flask import Blueprint
import json
class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
    Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
    Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world")
]

book_bp = Blueprint("book",__name__)

@book_bp.get("/book")
def print_first_book_info():
    dictionary_list = []
    for book in books: 
        book_dictionary = {
            "id" : book.id ,
            "title" : book.title,
            "description" : book.description
        }
        dictionary_list.append(book_dictionary)
    return dictionary_list[0]

