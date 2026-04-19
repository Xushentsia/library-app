from sqlalchemy import Column, Integer, String, Text  # Импорт типов данных для полей таблицы
from database import Base   # Импорт базового класса (шаблона) из database.py

class Book(Base):
    __tablename__ = "books" # Имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    year = Column(Integer)
    description = Column(String)


# Как SQLAlchemy преобразует это в SQL:

# CREATE TABLE books (
#   id SERIAL PRIMARY KEY,
#   title VARCHAR(200) NOT NULL,
#   author VARCHAR(100) NOT NULL,
#   year INTEGER,
#   description TEXT
# );