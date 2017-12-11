import json

from recipes import app, db
from .basetest import BaseTestCase

class TestGetUsers(BaseTestCase):
    """ Test get users"""
    def test_get_all_users(self):
            response = self.client.get('/users', headers=self.headers)
            self.assertIn('geom@gmail.com', str(response.data))
            self.assertEqual(response.status, "200 OK")

    def test_one_user(self):
        """ Test one users"""
        response = self.client.get('/users/5xxxxx', headers=self.headers)
        self.assertIn('geom@gmail.com', str(response.data))
        self.assertEqual(response.status, "200 OK")

    def test_unavailable_user(self):
        """ Test unavailable_user"""
        response = self.client.get('/users/jhdfjjhdff', headers=self.headers)
        self.assertIn('User not found', str(response.data))
        self.assertEqual(response.status, "404 NOT FOUND")
        
    def test_delete_users(self):
        """ Test delete_users"""
        response = self.client.delete(
            '/users/5xxxxx',
            data=self.user_test,
            headers=self.headers)
        self.assertIn(
            'There are recipes attached to this user! Deletion failed', str(
                response.data))
        self.assertEqual(response.status_code, 401)
    def test_delete_unavailable_users(self):
        """Test delete_unavailable_users"""
        response = self.client.delete(
            '/users/hjdfhjfdh',
            data=self.user_test,
            headers=self.headers)
        self.assertIn('User not available', str(response.data))
        self.assertEqual(response.status_code, 404)