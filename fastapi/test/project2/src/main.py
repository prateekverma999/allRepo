from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randint

app = FastAPI()

# Define the Pydantic model for the post structure
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int = None

my_post = [{
    "title": "Hello, World!",
    "content": "This is a sample post.",
    "published": True,
    "rating": 5
},{
    "title": "Another Post",
    "content": "This is another sample post.",
    "published": False,
    "rating": 3
}]

# Basic health check route
@app.get("/")
def post():
    return {"post": my_post}

# Handle POST request with raw dictionary input (not recommended for production)
@app.post("/post")
def create_post(post: dict = Body(...)):
    print(f"title = {post['title']}")
    return {"post": post}


@app.post("/create_post")
def create_post_v2(postv2: Post):
    post_dict = postv2.dict()
    post_dict["id"] = randint(0, 100000)
    my_post.append(post_dict)
    return {"post": post_dict}

