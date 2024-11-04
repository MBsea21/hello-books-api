
from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db

bp = Blueprint("bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    response = new_book.to_dict()
    return response, 201

@bp.get("")
def get_books():
    
    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    sort_param = request.args.get("sort")

    if sort_param: 
        attribute = validate_attribute(sort_param)
        query = query.order_by(attribute)
    else: 
        query = query.order_by(Book.id)
    
    books = db.session.scalars(query)

    books_response = []
    for book in books: 
        books_response.append(book.to_dict())
    return books_response

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)
    return book.to_dict()

def validate_book (book_id):
    try: 
        book_id = int(book_id)
    except: 
        response = ({"message": f"book {book_id} invalid"}, 400)
        abort(make_response(response))
    
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book: 
        response = ({"message": f"book {book_id} not found"},404)
        abort(make_response((response)))
    
    return book

@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    response_body = {"message": f"Book #{book_id} successfully updated"}

    return response_body


@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
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
