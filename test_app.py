import pytest
import requests
from run import app

@pytest.fixture
def client():
    # Настройка клиента Flask для тестирования
    with app.test_client() as client:
        yield client

def test_get_form(client):
    # Тестирование GET-запроса
    response = client.get('/')
    assert response.status_code == 200

#def test_post_valid_book(client):
#    response = client.post('/books', data={
#        'title': 'Война и мир',
#        'author': 'Лев Толстой'
#    }, follow_redirects=True)
#    assert response.status_code == 200

def test_update_book(client):
    response = client.post("/books/update", data={
        'id': '7',
        'new_title': 'новое123123123',
        'new_author': 'новое123123123',
    }, follow_redirects=True)

    assert response.status_code == 200

def test_delete_book(client):
    response = client.post("/books/delete/13")
    assert response.status_code == 302