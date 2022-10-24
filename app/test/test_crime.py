from fastapi.testclient import TestClient

from api import crime

client = TestClient(crime.router)


def test_crimes():
    response = client.get("/crimes")
    assert response.status_code == 200


def test_crimes_with_type():
    response = client.get("/crimes?crime_type=HOMICIDE")
    assert response.status_code == 200


def test_crimes_with_date():
    response = client.get("/crimes?crime_date=2015-01-01")
    assert response.status_code == 200


def test_crimes_with_type_and_date():
    response = client.get("/crimes?crime_date=2015-01-01&crime_type=HOMICIDE")
    assert response.status_code == 200
