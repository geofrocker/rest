import json

from recipes import app, db
from .basetest import BaseTestCase

class TestGetRecipe(BaseTestCase):
    def test_get_recipes(self):
            response = self.client.get('/', headers=self.headers)
            self.assertIn('Recipe One', str(response.data))
            self.assertEqual(response.status, "200 OK")
    def test_get_page(self):
            response = self.client.get('/?page=1', headers=self.headers)
            self.assertIn('Recipe One', str(response.data))
    def test_search(self):
            response = self.client.get('/?q=Recipe', headers=self.headers)
            self.assertIn('Recipe One', str(response.data))
    def test_search2(self):
            response = self.client.get('/?q=Rechjkkipe', headers=self.headers)
            self.assertIn('No recipes found', str(response.data))
            
    def test_get_recipe(self):
        response = self.client.get('/5xxxxx', headers=self.headers)
        self.assertIn('Ingredient one and two', str(response.data))

    def test_get_unavailable_recipe(self):
        response = self.client.get('/hjsdhjsddhj', headers=self.headers)
        self.assertIn('Recipe Not found', str(response.data))
        self.assertEqual(response.status, "404 NOT FOUND")

    def test_unauthorised_access(self):
        response = self.client.post('/', data=json.dumps(self.recipe_test))
        self.assertIn('Unauthorised access! Please log in', str(response.data))
    def test_invalid_token(self):
        headers = {'x-access-token': 'sdsdjhjkdsjkdsjkdsjkds',
                'Content-Type': 'application/json',
                }
        response = self.client.post(
            '/',
            content_type='application/json',
            data=json.dumps(
                []),
            headers=headers)
        self.assertIn('Invalid Token', str(response.data))
        self.assertEqual(response.status_code, 401)
    
class TestRecipeActivity(BaseTestCase):
    def test_add_recipe_successful(self):
        response = self.client.post(
            '/',
            data=json.dumps(
                self.recipe_test),
            headers=self.headers)
        self.assertIn('Recipe Created', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_add_with_unclean_data(self):
        response = self.client.post(
            '/',
            data=json.dumps(
                self.recipe_test3),
            headers=self.headers)
        self.assertIn('Populate all the required', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_add_with_an_existing_title(self):
        self.client.post(
            '/',
            data=json.dumps(
                self.recipe_test),
            headers=self.headers)
        response = self.client.post(
            '/',
            data=json.dumps(
                self.recipe_test4),
            headers=self.headers)
        self.assertIn('Title already exists', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_no_data_submitted(self):
        response = self.client.post(
            '/',
            content_type='application/json',
            data=json.dumps(
                []),
            headers=self.headers)
        
        self.assertIn('No data submitted', str(response.data))
    
    def test_missing_fields(self):
        response = self.client.post(
            '/',
            content_type='application/json',
            data=json.dumps(
                self.recipe_test2),
            headers=self.headers)
        self.assertIn('Populate all the required fields', str(response.data))
        
    def test_edit_recipe(self):
        response = self.client.put(
            '/5xxxxx',
            data=json.dumps(
                self.recipe_test),
            headers=self.headers)
        self.assertIn('Recipe Edited successfully', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_upvote_a_recipe(self):
        response = self.client.get(
            '/recipe/upvote/5xxxxx',
            headers=self.headers)
        self.assertIn('You should be redirected automatically', str(response.data))
        self.assertEqual(response.status_code, 302)

    def test_review_a_recipe(self):
        response = self.client.post(
            '/recipe/review/5xxxxx',
            data=json.dumps({'content':'My review'}),
            headers=self.headers)
        self.assertIn('You should be redirected automatically', str(response.data))
        self.assertEqual(response.status_code, 302)

    def test_edit_unavilable_recipe(self):  
        response = self.client.put(
            '/khjsdjkwjkwd',
            data=json.dumps(
                self.recipe_test),
            headers=self.headers)
        self.assertIn('Recipe not available', str(response.data))
        self.assertEqual(response.status_code, 404)

    def test_delete_recipe(self):
        response = self.client.delete(
            '/5xxxxx',
            data=json.dumps(
                self.recipe_test),
            headers=self.headers)
        self.assertIn('You should be redirected automatically', str(response.data))
        self.assertEqual(response.status_code, 302)

    def test_delete_unavilable_recipe(self):
        response = self.client.delete(
            '/khjsdjkwjkwd',
            data=json.dumps(
                self.recipe_test),
            headers=self.headers)
        
        self.assertIn('Recipe not available', str(response.data))
        self.assertEqual(response.status_code, 404)
class MyRecipes(BaseTestCase):
    def test_my_recipes_end_point(self):
        response = self.client.get('/myrecipes', headers=self.headers)
        self.assertIn('Ingredient one and two', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        """Test if the user has submitted search query"""
        response = self.client.get(
            '/myrecipes?q=hdsahhajsdhjds',
            headers=self.headers)
        self.assertIn('Recipe One', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_search_unvailable_recipe(self):
        self.client.post(
            '/',
            data=json.dumps(
                self.recipe_test),
            headers=self.headers)
        response = self.client.get(
            '/myrecipes?q=Recipe One',
            headers=self.headers)
        self.assertIn('Recipe One', str(response.data))
        self.assertEqual(response.status_code, 200)

