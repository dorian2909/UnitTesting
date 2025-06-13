
import unittest
import json
from main import app



class testing(unittest.TestCase):
    '''Se logra acceder a los endpoints y no tener que iniciar el archivo main para realizar pruebas'''
    def setUp(self):
        self.client = app.test_client()

    #funcion de post
    def test_artesanoPostTest(self):
        #payload
        artesano = {  
            "artesano": {
             'custom_id': "12",
            'nombre_completo': "Rick Sanchez",
            'email': "Rick@gmail.com",
            'telefono': "2121212",
            'direccion': "Tierra c136 en la avenida los morty",
            'categorias': ["arte cientifica"]
            }
        }
          #consulta post
        response = self.client.post('/artesano', 
            data=json.dumps(artesano), 
            content_type='application/json')
        # el response tiene que ser 201 y si lo es la prueba es exitosa
        self.assertEqual(response.status_code, 201)
        # ¿los datos devueltos estan contenidos en el nombre del artesano? osea "a" esta contenido en "b"? 
        #si es verdadero la prueba es exitosa
        self.assertIn('Rick Sanchez', response.get_data(as_text=True))
        
        
    def test_artesanoGetTest(self):
        #en las pruebas unitarias cada funcion tiene que ser independiente de cualquier otra funcion
        #por eso en este get volvemos a invocar un post
        artesano = {  
            "artesano": {
             'custom_id': "13",
            'nombre_completo': "Zoomer Smith",
            'email': "Zoomer@gmail.com",
            'telefono': "2121212",
            'direccion': "Tierra c136 en la avenida los morty",
            'categorias': ["arte cientifica"]
            }
        }
          
        response = self.client.post('/artesano', 
            data=json.dumps(artesano), 
            content_type='application/json')
        #get endpoint
        response = self.client.get('/artesano', content_type='application/json')
        
        # el response tiene que ser 200 y si lo es la prueba es exitosa
        self.assertEqual(response.status_code, 200)

        # ¿los datos devueltos estan contenidos en el nombre del artesano? osea "a" esta contenido en "b"? 
        #si es verdadero la prueba es exitosa
        self.assertIn('Zoomer Smith', response.get_data(as_text=True))
        

    def test_artesanoDeleteTest(self):
        artesano = {  
            "artesano": {
             'custom_id': "14",
            'nombre_completo': "Mortty Smith",
            'email': "Zoomer@gmail.com",
            'telefono': "2121212",
            'direccion': "Tierra c136 en la avenida los morty",
            'categorias': ["arte cientifica"]
            }
        }
          
        response = self.client.post('/artesano', 
            data=json.dumps(artesano), 
            content_type='application/json')
      #delete endpoint
        response = self.client.delete('/artesano/14', content_type='application/json')
    
        #si el response es 200, entonces la prueba es exitosa
        self.assertEqual(response.status_code, 200)
  
        #extraemos la respuesta
        response_data = response.get_json()
        #la api devuelve un booleano, entonces si response_data es igual a un true la prueba es exitosa
        self.assertEqual(response_data, {'result': True})
        



if __name__ == '__main__':
    unittest.main()
    #se ejecuta con unittest para que cada funcion que empieze con test se ejecuten


     