from flask import Blueprint
hello_world_bp = Blueprint("hello_world", __name__)
@hello_world_bp.get("/")
def first_endpoint():
    say_hello_world = "Hello, World!"
    return say_hello_world

@hello_world_bp.get("/hello/JSON")
def say_hello_json():
    return {
        "name" : "Ada Lovelace",
        "message" : "Hello!",
        "hobbies" : ["Fishing", "Swimming", "Watching Reality Shows"]
    }
@hello_world_bp.get("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"].append(new_hobby)
    return response_body
# @hello_world_bp.get("/broken-endpoint-with-broken-server-code")
# def broken_endpont():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body