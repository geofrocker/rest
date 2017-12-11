import json

from recipes import app, db
from .basetest import BaseTestCase


class TestUserReg(BaseTestCase):
    """
    The user registration
    """
    def test_user_registration_success(self):
        """
        The user_registration_success
        """
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test))
        self.assertIn('Your are now registered! You can log in', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_user_submits_no_data(self):
        """
        The user submits no data
        """
        response = self.client.post('/auth/register')
        self.assertIn('No data submitted', str(response.data))
        self.assertEqual(response.status_code, 401)
    
    def test_user_submits_missing_fields(self):
        """
        The user_submits_missing_fields
        """
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test2))
        self.assertIn('Populate all the fields', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_user_submits_invalid_data(self):
        """
        The user_submits_invalid_data
        """
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test4))
        self.assertIn('Please enter a valid name', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_user_submits_invalid_email(self):
        """
        The user_submits_invalid_email
        """
        response = self.client.post('/auth/register',
                                    content_type='application/json',
                                    data=json.dumps(
                                        self.user_test3))
        self.assertIn('Please enter a valid email', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_user_sumit_an_already_used_email(self):
        """
        The user_sumit_an_already_used_email
        """
        self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test))
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test))
        self.assertIn('Email already exists', str(response.data))
        self.assertEqual(response.status_code, 400)

class TestUserLogin(BaseTestCase):
    """
    The user login
    """
    def test_user_login_success(self):
        """
        The user login success
        """
        self.client.post('/auth/register', content_type='application/json',
                         data=json.dumps(self.user_test))
        response = self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(
                self.user2))
        self.assertTrue(response)

    def test_wrong_username(self):
        """
        The wrong username
        """
        response = self.client.post('/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "geomssd",
                                                      "password": '12345'}))
        self.assertIn('User does not exist', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_wrong_password(self):
        """
        The wrong password
        """
        response = self.client.post('/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "geof",
                                                      "password": '12345hyuywe'}))
        self.assertIn('Invalid password', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_no_data_submitted(self):
        """
        The no data submitted
        """
        response = self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(
                {}))
        
        self.assertIn(
            'Please enter your username and password', str(
                response.data))
        self.assertEqual(response.status_code, 400)