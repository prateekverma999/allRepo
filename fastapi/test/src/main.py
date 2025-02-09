from fastapi import FastAPI
from Database import database, model
from routs import user, post


app = FastAPI()

# Ensure database tables are created
model.Base.metadata.create_all(bind=database.engine)

app.include_router(post.router) # Add this line to include the post router
app.include_router(user.router) # Add this line to include the user router

