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