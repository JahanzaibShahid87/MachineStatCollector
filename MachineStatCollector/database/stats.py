""" Database model for saving stats of client servers
"""


from sqlalchemy import Column, Integer, Text, ForeignKey, Float
from database import Base


class Stats(Base):
    """The ORM model for stats
    """

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, nullable=False, unique=True,
                autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    memory_usage = Column(Float)
    cpu_usage = Column(Float)
    uptime = Column(Text)
