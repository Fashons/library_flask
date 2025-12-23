import pytest
from run import app
from app.model.book import BookRepo, Book
from app.model.user import UserRepo


# Фикстура для очистки тестовых данных после выполнения
@pytest.fixture(scope='module', autouse=True)
def cleanup():
    yield
    # Очистка тестовых данных после всех тестов
    with app.app_context():
        repo = BookRepo()
        test_books = repo.all()
        for book in test_books:
            if book.title.startswith("Тестовая книга"):
                repo.delete(book.id)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def repo():
    return BookRepo()


# Фикстура для аутентификации
@pytest.fixture
def logged_in_client(client):
    # Создаем тестового пользователя если его нет
    with app.app_context():
        user_repo = UserRepo()
        if not user_repo.get_by_username('test_user'):
            user_repo.add('test_user', 'password123')

    # Аутентифицируемся
    client.post('/auth/login', data={
        'username': 'test_user',
        'password': 'password123'
    }, follow_redirects=True)

    yield client

    # Выходим после тестов
    client.get('/auth/logout', follow_redirects=True)


def test_create_book(logged_in_client, repo):
    # CREATE: Добавляем новую книгу
    response = logged_in_client.post('/books', data={
        'title': 'Тестовая книга CREATE',
        'author': 'Тестовый автор CREATE'
    }, follow_redirects=True)

    assert response.status_code == 200
    # Проверяем, что книга добавилась
    with app.app_context():
        books = repo.all()
        assert any(book.title == "Тестовая книга CREATE" for book in books)


def test_read_books(logged_in_client):
    # READ: Проверяем отображение списка книг
    response = logged_in_client.get('/books/')
    assert response.status_code == 200
    assert "Мои книги".encode('utf-8') in response.data


def test_update_book(logged_in_client, repo):
    # Сначала создаем книгу для обновления
    with app.app_context():
        repo.add("Тестовая книга UPDATE", "Тестовый автор UPDATE")
        books = repo.all()
        test_book = next(book for book in books if book.title == "Тестовая книга UPDATE")

    # UPDATE: Обновляем книгу
    response = logged_in_client.post("/books/update", data={
        'id': str(test_book.id),
        'new_title': 'Обновленная тестовая книга',
        'new_author': 'Обновленный автор',
    }, follow_redirects=True)

    assert response.status_code == 200

    # Проверяем, что книга обновилась
    with app.app_context():
        updated_book = repo.get_by_id(test_book.id)
        assert updated_book is not None
        assert updated_book.title == "Обновленная тестовая книга"
        assert updated_book.author == "Обновленный автор"


def test_delete_book(logged_in_client, repo):
    # Сначала создаем книгу для удаления
    with app.app_context():
        repo.add("Тестовая книга DELETE", "Тестовый автор DELETE")
        books = repo.all()
        test_book = next(book for book in books if book.title == "Тестовая книга DELETE")
        book_id = test_book.id

    # DELETE: Удаляем книгу
    response = logged_in_client.post(f"/books/delete/{book_id}", follow_redirects=True)
    assert response.status_code == 200

    # Проверяем, что книга удалена
    with app.app_context():
        assert repo.get_by_id(book_id) is None