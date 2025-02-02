from sqlalchemy import Column, Integer, String, Boolean
from .database import base


class Post(base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default='TRUE', nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))