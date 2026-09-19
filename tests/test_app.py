import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get("/")

    assert response.status_code == 200


def test_index_contains_title(client):
    response = client.get("/")

    text = response.get_data(as_text=True)

    assert "Калькулятор квадратного корня" in text


def test_calculate_positive_real(client):
    response = client.post(
        "/",
        data={
            "real": "25",
            "imag": "",
            "precision": "50",
            "display_digits": "10"
        }
    )

    assert response.status_code == 200

    text = response.get_data(as_text=True)

    assert "5" in text
    assert "-5" in text


def test_calculate_negative_real(client):
    response = client.post(
        "/",
        data={
            "real": "-25",
            "imag": "",
            "precision": "50",
            "display_digits": "10"
        }
    )

    assert response.status_code == 200

    text = response.get_data(as_text=True)

    assert "5i" in text
    assert "-5i" in text


def test_calculate_complex(client):
    response = client.post(
        "/",
        data={
            "real": "3",
            "imag": "4",
            "precision": "50",
            "display_digits": "10"
        }
    )

    assert response.status_code == 200

    text = response.get_data(as_text=True)

    assert "2 + i" in text
    assert "-2 - i" in text


def test_calculate_negative_imaginary(client):
    response = client.post(
        "/",
        data={
            "real": "3",
            "imag": "-4",
            "precision": "50",
            "display_digits": "10"
        }
    )

    assert response.status_code == 200

    text = response.get_data(as_text=True)

    assert "2 - i" in text
    assert "-2 + i" in text


def test_empty_real(client):
    response = client.post(
        "/",
        data={
            "real": "",
            "imag": "",
            "precision": "50",
            "display_digits": "10"
        }
    )

    assert response.status_code == 200

    text = response.get_data(as_text=True)

    assert "Введите действительную или мнимую часть числа." in text



def test_invalid_precision(client):
    response = client.post(
        "/",
        data={
            "real": "25",
            "imag": "",
            "precision": "abc",
            "display_digits": "10"
        }
    )

    assert response.status_code == 200

    text = response.get_data(as_text=True)

    assert "Точность и количество отображаемых знаков должны быть целыми числами." in text


def test_invalid_display_digits(client):
    response = client.post(
        "/",
        data={
            "real": "25",
            "imag": "",
            "precision": "50",
            "display_digits": "abc"
        }
    )

    assert response.status_code == 200

    text = response.get_data(as_text=True)

    assert "Точность и количество отображаемых знаков должны быть целыми числами." in text


def test_values_remain_after_error(client):
    response = client.post(
        "/",
        data={
            "real": "",
            "imag": "4",
            "precision": "100",
            "display_digits": "20"
        }
    )

    text = response.get_data(as_text=True)

    assert 'value="4"' in text
    assert 'value="100"' in text
    assert 'value="20"' in text
