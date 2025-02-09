from fastapi import FastAPI, Depends, Query
from sqlalchemy import asc, desc
from Database import database, model
from routs import user, post


app = FastAPI()

# Ensure database tables are created
model.Base.metadata.create_all(bind=database.engine)

app.include_router(post.router) # Add this line to include the post router
app.include_router(user.routs) # Add this line to include the user router

