import json
from tests.basetest import BaseTestCase

class Tests(BaseTestCase):
    def test_register(self):
        response = self.client.post('/auth/register', data=self.user_test)
        assert response.status == "200 OK"

    def test_recipes(self):
        response = self.client.get('/', headers=self.headers)
        assert response.status == "200 OK"

    def test_recipe(self):
        response = self.client.get('/5xxxxx', headers=self.headers)
        assert response.status == "200 OK"

    def test_add_recipe(self):
        response = self.client.post('/', data=json.dumps(self.recipe_test), headers=self.headers)
        assert response.status == "200 OK"

    def test_edit_recipe(self):
        response = self.client.put('/5xxxxx', data=json.dumps(self.recipe_test), headers=self.headers)
        assert response.status == "200 OK"

    def test_delete_recipe(self):
        response = self.client.delete('/5xxxxx', data=json.dumps(self.recipe_test), headers=self.headers)
        assert response.status == "200 OK"

    def test_get_all_users(self):
        response = self.client.get('/users', headers=self.headers)
        assert response.status == "200 OK"

    def test_one_user(self):
        response = self.client.get('/users/5xxxxx', headers=self.headers)
        assert response.status == "200 OK"

    def test_delete_users(self):
        response = self.client.delete('/users/5xxxxx', data=self.user_test, headers=self.headers)
        assert response.status == "200 OK"
        