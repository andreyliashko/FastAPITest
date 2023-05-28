from fastapi import FastAPI, Query
from scremas import Book
from typing import List

app = FastAPI()


@app.get('/')
def hello():
    return {'key': 'hello'}


@app.get('/{pk}')
def get_item(pk: int, q: str = None):
    return {'key': pk, 'q': q}


@app.get('/user/{user_id}/items/{item}/')
def get_item(user_id: int, item: str):
    return {'id': user_id, 'items': item}


@app.post('/book/')
def create_new_book(item: Book):
    return item


@app.get('/book/')
def get_book(query: List[str] = Query(None, min_length=1, max_length=10, description='search book')):
    return query
