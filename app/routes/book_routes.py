
from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book,request_body)

@bp.get("")
def get_books():
    request_arguments = request.args
    return get_models_with_filters(Book,request_arguments)

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict()

# def validate_book (book_id):
#     try: 
#         book_id = int(book_id)
#     except: 
#         response = ({"message": f"book {book_id} invalid"}, 400)
#         abort(make_response(response))
    
#     query = db.select(Book).where(Book.id == book_id)
#     book = db.session.scalar(query)

#     if not book: 
#         response = ({"message": f"book {book_id} not found"},404)
#         abort(make_response((response)))
    
#     return book

@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    response_body = {"message": f"Book #{book_id} successfully updated"}

    return response_body


@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    response_body = {"message":f"Book #{book_id} successfully deleted"}
    return response_body


def validate_attribute(attribute): 
    try: 
        attribute = getattr(Book,attribute)
    except: 
        response = ({"message": f"{attribute} key invalid"}, 400)
        abort(make_response(response))
    return attribute
