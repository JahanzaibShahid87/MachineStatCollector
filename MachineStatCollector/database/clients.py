""" Database model for saving client's information
"""


from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, Enum
from database import Base


class Client(Base):
    """The ORM model for clients
    """

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, nullable=False, unique=True,
                autoincrement=True)

    username = Column(Text)
    ip = Column(Text)
    email = Column(Text)
    port = Column(Integer)
    cpu_limit = Column(Integer)
    memory_limit = Column(Integer)
