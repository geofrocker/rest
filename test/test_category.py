import json

from recipes import app, db
from .basetest import BaseTestCase

class TestCategory(BaseTestCase):
    """
    Test category operations
    """
    def test_get_categories(self):
        """
        Test  get category 
        """
            response = self.client.get('/category', headers=self.headers)
            self.assertIn('General recpes', str(response.data))
            self.assertEqual(response.status, "200 OK")

    def test_post_category(self):
        """
        test post category
        """
        response = self.client.post(
            '/category',
            data=json.dumps(
                self.cat_test),
            headers=self.headers)
        self.assertIn('Category Created', str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_post_category_with_no_data(self):
        """
        test post category
        """
        response = self.client.post('/category', data=json.dumps([]),
                                     headers=self.headers)
        self.assertIn('No data submitted', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_post_category_with_missing_fields(self):
        """
        test post category with missing fields
        """
        response = self.client.post('/category', data=json.dumps(self.cat_test2),
                                     headers=self.headers)
        self.assertIn('Please populate all fields', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_post_category_with_invalid_data(self):
        """
        test post category with invalid_data
        """
        response = self.client.post('/category', data=json.dumps(self.cat_test3),
                                     headers=self.headers)
        self.assertIn('Please populate all fields', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_post_category_with_same_name(self):
        """
        test post category with same_name
        """
        self.client.post('/category', data=json.dumps(self.cat_test),
                                     headers=self.headers)
        response = self.client.post('/category', data=json.dumps(self.cat_test),
                                     headers=self.headers)
        self.assertIn('Category name already exists', str(response.data))
        self.assertEqual(response.status_code, 400)

class TestCategoryActivity(BaseTestCase):
    """
    Test get,edit and delete category
    """
    def test_get_category(self):
        """
        Test get category
        """
        response = self.client.get('/category/5xxxxx', headers=self.headers)
        self.assertIn('General recpes', str(response.data))
        self.assertEqual(response.status, "200 OK")

    def test_edit_category(self):
        """
        Test edit category
        """
        response = self.client.put(
            '/category/5xxxxx',
            data=json.dumps(
                self.cat_test),
            headers=self.headers)
        self.assertIn(
            'Cannot edit recipe because there a recipes attached to it', str(
                response.data))
        self.assertEqual(response.status_code, 400)

    def test_delete_category(self):
        """
        Test delete category
        """
        response = self.client.delete(
            '/category/5xxxxx',
            data=json.dumps(
                self.cat_test),
            headers=self.headers)
        self.assertIn(
            'Category has recipes attached to it. Deletion failed', str(
                response.data))
        self.assertEqual(response.status_code, 401)