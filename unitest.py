
import unittest
import json
from main import app
class testing(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


    def test_artesanoPostTest(self):
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
          
        response = self.client.post('/artesano', 
            data=json.dumps(artesano), 
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Rick Sanchez', response.get_data(as_text=True))
        
        
    def test_artesanoGetTest(self):
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
        response = self.client.get('/artesano', content_type='application/json')
        
  
        self.assertEqual(response.status_code, 200)

        # ¿los datos devueltos incluyen el nombre del artesano?
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
      
        response = self.client.delete('/artesano/14', content_type='application/json')
    

        self.assertEqual(response.status_code, 200)
  
 
        response_data = response.get_json()
        self.assertEqual(response_data, {'result': True})
        




    
        

if __name__ == '__main__':
    unittest.main()


     