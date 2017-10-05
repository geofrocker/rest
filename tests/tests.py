import json
from tests.basetest import BaseTestCase

class Recipes(BaseTestCase):
    def test_get_recipes(self):
        response = self.client.get('/')
        assert response.status == "200 OK"
