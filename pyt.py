import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_post(client):
     response =client.post("/artesano", json={  
            "artesano": {
             'custom_id': "12",
            'nombre_completo': "Rick Sanchez",
            'email': "Rick@gmail.com",
            'telefono': "2121212",
            'direccion': "Tierra c136 en la avenida los morty",
            'categorias': ["arte cientifica"]
            }
        })
     #assert response.status_code == 200
     assert "Rick Sanchez" in response.get_data("nombre_completo")
    # assert response.status_code == 201

def test_get(client):
     
     response =client.post("/artesano", json={  
            "artesano": {
             'custom_id': "12",
            'nombre_completo': "Rick Sanchez",
            'email': "Rick@gmail.com",
            'telefono': "2121212",
            'direccion': "Tierra c136 en la avenida los morty",
            'categorias': ["arte cientifica"]
            }
        })
     response = client.get("/artesano")
     assert response.status_code == 200


def test_delete(client):
     
     response =client.post("/artesano", json={  
            "artesano": {
             'custom_id': "14",
            'nombre_completo': "Jerry Smith",
            'email': "Rick@gmail.com",
            'telefono': "2121212",
            'direccion': "Tierra c136 en la avenida los morty",
            'categorias': ["arte cientifica"]
            }
        })
     response = client.delete("/artesano/14")
     data = response.get_json()
     assert data["result"] is True