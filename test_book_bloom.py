from fastapi.testclient import TestClient

from book_bloom.main import app, init_db


init_db()
client = TestClient(app)


def test_list_books():
    response = client.get("/api/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_search_books():
    response = client.get("/api/books/search", params={"q": "hobbit"})
    assert response.status_code == 200
    data = response.json()
    assert any("Hobbit" in book["title"] for book in data)
