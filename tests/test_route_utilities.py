from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
from werkzeug.exceptions import HTTPException
from app.models.book import Book
from app.models.author import Author
import pytest

# We use the `client` fixture because we need an
# application context to work with the database session
def test_create_model_book(client):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    result = create_model(Book, test_data)
    result_body = result.get_json()
    print( "RESULT IS : \n", result)
    # print("RESULT BODY IS : \n", result_body)
    # print("RESULT BODY TYPE IS :\n", type(result_body))
    # print( "EXPECTED WAS :\n", {
    #     "id": 1,
    #     "title": "New Book",
    #     "description": "The Best!"
    # } )
    
    # Assert
    assert result.status_code == 201
    assert result_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"}

def test_create_model_book_missing_data(client):
    # Arrange
    test_data = {
        "description": "The Best!"
    }

    # Act & Assert
    # Calling `create_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as error:
        result_book = create_model(Book, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"

def test_create_model_author(client):
    # Arrange
    test_data = {
        "name": "New Author"
    }

    # Act
    result = create_model(Author, test_data)

    # Assert
    assert result.status_code == 201
    assert result.get_json() == {
        "id": 1,
        "name": "New Author"
    }

def test_get_models_with_filters_one_matching_book(two_saved_books):
    # Act
    result = get_models_with_filters(Book, {"title": "ocean"})

    # Assert
    assert result == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }]