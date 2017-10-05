import json
from tests.basetest import BaseTestCase

class Auth(BaseTestCase):
    """
    tests on user registration
    """

    def test_login(self):
        response = self.client.post("/auth/register",data= self.user)
        response = self.client.post("/auth/login",data= self.user)
        assert response.status=="401 UNAUTHORIZED"
