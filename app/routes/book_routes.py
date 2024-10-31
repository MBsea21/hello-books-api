
from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    print("line 10")
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201

@books_bp.get("")
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
        books_response.append(get_dict(book))
    return books_response

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)
    return get_dict(book)


def get_dict(book): 
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

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

@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_attribute(attribute): 
    try: 
        attribute = getattr(Book,attribute)
    except: 
        response = ({"message": f"{attribute} key invalid"}, 400)
        abort(make_response(response))
    return attribute
