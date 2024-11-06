from app.models.book import Book
import pytest
#test_data
# book titles
book_1_title = "Ocean Book"
book_2_title = "Mountain Book"
book_3_title = "Lake Book"


#book descriptions: 
book_1_description ="watr 4evr"
book_2_description ="i luv 2 climb rocks"
book_3_description ="lets go swim"

def KV_pair(key,value):
    dictionary = {key: value}
    return dictionary

k1 = "title"
k2 = "description"

book_1 = KV_pair(k1,book_1_title), KV_pair(k2,book_1_description)
book_2 = KV_pair(k1,book_2_title), KV_pair(k2,book_2_description)
book_3 =KV_pair(k1,book_3_title), KV_pair(k2,book_3_description)
###########################################################################
######################## test get all books ##################################
###########################################################################
# When we have records, `get_all_books` returns a list containing a dictionary representing each `Book`
def test_get_all_books_with_two_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    assert response_body[1] == {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
    }

# When we have records and a `title` query in the request arguments, `get_all_books` returns a list containing only the `Book`s that match the query
def test_get_all_books_with_title_query_matching_none(client, two_saved_books):
    # Act
    data = {'title': 'Desert Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# When we have records and a `title` query in the request arguments, `get_all_books` returns a list containing only the `Book`s that match the query
def test_get_all_books_with_title_query_matching_one(client, two_saved_books):
    # Act
    data = {'title': 'Ocean Book'}
    response = client.get("/books", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []



###########################################################################
######################## test get 1 book ##################################
###########################################################################


def test_get_one_book(client, two_saved_books):
    response = client.get("/books/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_get_non_existent_book(client, two_saved_books):
    response = client.get("/books/4")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": f"Book 4 not found"}

def test_get_book_invalid_input(client, two_saved_books):
    response = client.get("/books/luv")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": f"Book luv invalid"}

# When we call `get_one_book` with a numeric ID that doesn't have a record, we get the expected error message
def test_get_one_book_missing_record(client, two_saved_books):
    # Act
    response = client.get("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

# When we call `get_one_book` with a non-numeric ID, we get the expected error message
def test_get_one_book_invalid_id(client, two_saved_books):
    # Act
    response = client.get("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}



###########################################################################
####################### test create book ##################################
###########################################################################

def test_create_one_book(client):
    response=client.post("/books",json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1, 
        "title": "New Book",
        "description": "The Best!"
    }

def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}
    
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {'message': 'Invalid request: missing title'}

def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Invalid request: missing description"}

def test_create_one_book_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }

###########################################################################
########################## test put book ##################################
###########################################################################

def test_put_book(client, two_saved_books):
    book_details = {
        "id": 1,
        "title": "New Book",
        "description": "The Best"
    }

    response = client.put("/books/1", json=book_details)
    response_body =  response.get_json()
    check_database = client.get("/books/1")
    check_database_response_body = check_database.get_json()
    print("RESPONSE BODY IS ", response_body)

    assert response.status_code == 200
    assert response_body["message"] == "Book #1 successfully updated"
    assert check_database.status_code == 200
    assert check_database_response_body == book_details


def test_update_book_with_extra_keys(client, two_saved_books):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.put("/books/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["message"] == "Book #1 successfully updated"

def test_update_book_missing_record(client, two_saved_books):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    response = client.put("/books/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

def test_update_book_invalid_id(client, two_saved_books):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    response = client.put("/books/cat", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}

###########################################################################
########################## test delete book ###############################
###########################################################################

def test_delete_book(client, two_saved_books):
    book_details = {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    pre_check_database = client.get("/books/1")
    pre_check_database_response_body = pre_check_database.get_json()
    response = client.delete("/books/1", json=book_details)
    post_check_database = client.get("/books/1")
    post_check_database_response_body = post_check_database.get_json()

    assert response.status_code == 204
    assert pre_check_database.status_code == 200
    assert pre_check_database_response_body == book_details
    assert post_check_database.status_code == 404
    assert post_check_database_response_body == {"message": "Book 1 not found"}

def test_delete_book(client, two_saved_books):
    # Act
    response = client.delete("/books/1")
    print("RESPONSE IS ", response)
    response_body = response.get_json()
    response_body_message = response_body["message"]

    # Assert
    assert response.status_code == 200
    assert response_body_message == "Book #1 successfully deleted"

def test_delete_book_missing_record(client, two_saved_books):
    # Act
    response = client.delete("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

def test_delete_book_invalid_id(client, two_saved_books):
    # Act
    response = client.delete("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}