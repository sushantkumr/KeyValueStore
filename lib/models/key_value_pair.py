from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.models.db import Base


class KeyValuePair(Base):
    __tablename__ = 'kay_value_pair'
    id = Column(Integer, primary_key=True)
    key = Column(String(20))
    value = Column(String(50))


    def __init__(self, key=None, value=None):
        """Constructor."""
        self.key = key
        self.value = value


    def __repr__(self):
        return '<KeyValuePair %r>' % (self.title)
