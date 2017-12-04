import json

from recipes import app, db
from .basetest import BaseTestCase


class TestUserReg(BaseTestCase):
    def test_user_registration_success(self):
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test))
        self.assertIn('Your are now registered! You can log in', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_user_submits_no_data(self):
        response = self.client.post('/auth/register')
        self.assertIn('No data submitted', str(response.data))
        self.assertEqual(response.status_code, 401)
    
    def test_user_submits_missing_fields(self):
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test2))
        self.assertIn('Populate all the fields', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_user_submits_invalid_data(self):
        response = self.client.post(
            '/auth/register',
            content_type='application/json',
            data=json.dumps(
                self.user_test4))
        self.assertIn('Please enter a valid name', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_user_submits_invalid_email(self):
        response = self.client.post('/auth/register',
                                    content_type='application/json',
                                    data=json.dumps(
                                        self.user_test3))
        self.assertIn('Please enter a valid email', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_user_sumit_an_already_used_email(self):
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
    def test_user_login_success(self):
        self.client.post('/auth/register', content_type='application/json',
                         data=json.dumps(self.user_test))
        response = self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(
                self.user2))
        self.assertTrue(response)

    def test_wrong_username(self):
        response = self.client.post('/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "geomssd",
                                                      "password": '12345'}))
        self.assertIn('User does not exist', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_wrong_password(self):
        response = self.client.post('/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "geof",
                                                      "password": '12345hyuywe'}))
        self.assertIn('Invalid password', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_no_data_submitted(self):
        response = self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(
                {}))
        
        self.assertIn(
            'Please enter your username and password', str(
                response.data))
        self.assertEqual(response.status_code, 400)