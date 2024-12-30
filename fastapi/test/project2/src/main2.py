from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randint

app = FastAPI()

class Post(BaseModel):
    name: str
    age: int
    city: str


my_post = [
    {
        "name": "ram",
        "age": 25,
        "city": "delhi"
    },
    {
        "name": "shyam",
        "age": 30,
        "city": "mumbai"
    }
    ]

@app.get('/')
def get_post():
    return {'post': my_post}



@app.post("/post")
def create_post(post:Post):
    new_post = post.dict()
    new_post["ID"] = randint(0,100000)
    my_post.append(new_post)
    return {'post': my_post}