import json
from .basetest import BaseTestCase
from recipes import app, db

class Tests(BaseTestCase):
    def test_register(self):
        response = self.client.post('/auth/register', content_type='application/json',
                                    data=json.dumps(self.user_test))
        response2 = self.client.post('/auth/register')
        self.assertIn('User Created', str(response.data))
        self.assertIn('No data submitted', str(response2.data))
        assert response.status_code == 201
        assert response2.status_code == 200 

    def test_login(self):
        response = self.client.post('/auth/login', content_type='application/json',
                                    data=json.dumps(self.user))
        response2 = self.client.post('/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "geomssd", "password": '12345'}))
        response3 = self.client.post('/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "geom", "password": '12345hyuywe'}))
        response4 = self.client.post('/auth/login', content_type='application/json',
                                    data=json.dumps({}))
        self.assertTrue(response)
        self.assertIn('Invalid user', str(response2.data))
        self.assertIn('Invalid password', str(response3.data))
        self.assertIn('Could not verify user', str(response4.data))

    def test_recipes(self):
        response = self.client.get('/', headers=self.headers)
        response2 = self.client.get('/?page=1', headers=self.headers)
        response3 = self.client.get('/?q=Recipe', headers=self.headers)
        self.assertIn('Recipe One', str(response.data))
        self.assertIn('Recipe One', str(response2.data))
        self.assertIn('Recipe One', str(response3.data))
        db.drop_all()
        db.create_all()
        response4 = self.client.get('/?q=Recipe', headers=self.headers)
        self.assertIn('No recipes found', str(response4.data))
        assert response.status == "200 OK"

    def test_recipe(self):
        response = self.client.get('/5xxxxx', headers=self.headers)
        response2 = self.client.get('/hjsdhjsddhj', headers=self.headers)
        self.assertIn('Ingredient one and two', str(response.data))
        self.assertIn('Recipe Not found', str(response2.data))
        assert response.status == "200 OK"
    
    def test_invalid_token_required(self):
        headers = {'x-access-token': 'sdsdjhjkdsjkdsjkdsjkds',
                        'Content-Type': 'application/json',
                        }
        response = self.client.post('/', data=json.dumps(self.recipe_test))
        response2 = self.client.post('/', content_type='application/json', data=json.dumps([]), headers=headers)
        self.assertIn('You have no access token', str(response.data))
        self.assertIn('Invalid Token', str(response2.data))
        assert response.status_code == 401
        assert response2.status_code == 401

    def test_add_recipe(self):
        response = self.client.post('/', data=json.dumps(self.recipe_test), headers=self.headers)
        response2 = self.client.post('/', content_type='application/json', data=json.dumps([]), headers=self.headers)
        self.assertIn('Recipe Created', str(response.data))
        self.assertIn('Recipe Creation failed', str(response2.data))
        assert response.status_code == 201

    def test_edit_recipe(self):
        self
        response = self.client.put('/5xxxxx', data=json.dumps(self.recipe_test),
                                   headers=self.headers)
        response2 = self.client.put('/khjsdjkwjkwd', data=json.dumps(self.recipe_test),
                                   headers=self.headers)
        self.assertIn('Recipe Edited successfully', str(response.data))
        assert response.status_code == 201
        self.assertIn('Recipe not available', str(response2.data))
        assert response2.status_code == 404

    def test_delete_recipe(self):
        response = self.client.delete('/5xxxxx', data=json.dumps(self.recipe_test),
                                      headers=self.headers)
        response2 = self.client.delete('/khjsdjkwjkwd', data=json.dumps(self.recipe_test),
                                   headers=self.headers)
        self.assertIn('Recipe Deleted successfully', str(response.data))
        self.assertIn('Recipe not available', str(response2.data))
        assert response.status_code == 200
        assert response2.status_code == 404

    def test_get_all_users(self):
        response = self.client.get('/users', headers=self.headers)
        self.assertIn('geom@gmail.com', str(response.data))
        assert response.status == "200 OK"

    def test_one_user(self):
        response = self.client.get('/users/5xxxxx', headers=self.headers)
        response2 = self.client.get('/users/jhdfjjhdff', headers=self.headers)
        self.assertIn('geom@gmail.com', str(response.data))
        self.assertIn('User not found', str(response2.data))
        assert response.status == "200 OK"

    def test_delete_users(self):
        response = self.client.delete('/users/5xxxxx', data=self.user_test, headers=self.headers)
        response2 = self.client.delete('/users/hjdfhjfdh', data=self.user_test, headers=self.headers)
        self.assertIn('User deleted', str(response.data))
        self.assertIn('User not available', str(response2.data))
        assert response.status == "200 OK"

    def test_get_categories(self):
        response = self.client.get('/category', headers=self.headers)
        self.assertIn('General recpes', str(response.data))
        assert response.status == "200 OK"

    def test_post_category(self):
        response = self.client.post('/category', data=json.dumps(self.cat_test),
                                    headers=self.headers)
        response2 = self.client.post('/category', data=json.dumps([]),
                                    headers=self.headers)
        self.assertIn('Category Created', str(response.data))
        self.assertIn('Category  Creation failed', str(response2.data))
        assert response.status == "200 OK"

    def test_get_category(self):
        response = self.client.get('/category/5xxxxx', headers=self.headers)
        self.assertIn('General recpes', str(response.data))
        assert response.status == "200 OK"

    def test_edit_category(self):
        response = self.client.put('/category/5xxxxx', data=json.dumps(self.cat_test),
                                   headers=self.headers)
        self.assertIn('Category Edited successfully', str(response.data))
        assert response.status == "200 OK"

    def test_delete_category(self):
        response = self.client.delete('/category/5xxxxx', data=json.dumps(self.cat_test),
                                      headers=self.headers)
        self.assertIn('Category Deleted successfully', str(response.data))
        assert response.status == "200 OK"

    def test_dashboard(self):
        response = self.client.get('/myrecipes', headers=self.headers)
        self.assertIn('No recipes found', str(response.data))
        assert response.status_code == 404
        self.client.post('/', data=json.dumps(self.recipe_test), headers=self.headers)
        response2= self.client.get('/myrecipes', headers=self.headers)
        self.assertIn('Recipe One', str(response2.data))
        assert response2.status_code == 200
        
    def test_search(self):    
        """Test if the user has submitted search query"""
        response = self.client.get('/myrecipes?q=hdsahhajsdhjds', headers=self.headers)
        self.assertIn('No recipes found', str(response.data))
        assert response.status_code == 404
        self.client.post('/', data=json.dumps(self.recipe_test), headers=self.headers)
        response2 = self.client.get('/myrecipes?q=Recipe One', headers=self.headers)
        self.assertIn('Recipe One', str(response2.data))
        assert response2.status_code == 200



        
        