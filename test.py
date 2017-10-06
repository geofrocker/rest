"""rest api/ test.py"""
from app import app

password = '12345'
user={'id':'5xxxxx', 'name':'Geofrey', 'username':'geom', 'email':'geom@gmail.com', 'password':password}
recipe={
"title":"Recipe two",
"ingredients":"Recipe One",
"steps":"Recipe One one",
"created_by":"d6ec3c95-19f8-43e0-9391-abb82a3c936e"
}
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM4NDM5NGYyLTcxZWYtNDZhOS1iOGQ1LWE5MWI4Yjk4MmMwZiIsImV4cCI6MTUwNzI1NDUwNX0.DnsMeUsIGK2hab4oXb4DRqegfhtB9osi0VF7UoAXErg'
headers = {'Authorization': 'Basic eyJ0eXAiOiJKV1QiLCJhb',
                        'Content-Type': 'application/json',
                        'x-access-token' : token
                        }

def test_home_end_point():
    """Test home page"""
    client = app.test_client()
    rsp = client.get('/')
    assert rsp.status == '200 OK'

def test_one_recipe_end_point():
    """Test one recipe"""
    client = app.test_client()
    rsp = client.get('/181c3c3bf-1ed2-4a10-bd40-c808baef9948',headers=headers)
    assert rsp.status == '401 UNAUTHORIZED'

def test_add_Recipe_end_point():
    """Test add_Recipe_end_point"""
    client = app.test_client()
    rsp = client.post('/', data=recipe)
    assert rsp.status == '401 UNAUTHORIZED'

def test_edit_Recipe_end_point():
    """Test edit_Recipe_end_point"""
    client = app.test_client()
    rsp = client.put('/181c3c3bf-1ed2-4a10-bd40-c808baef9948',data=recipe)
    assert rsp.status == '401 UNAUTHORIZED'

def test_delete_Recipe_end_point():
    """Test delete_Recipe_end_point"""
    client = app.test_client()
    rsp = client.delete('/181c3c3bf-1ed2-4a10-bd40-c808baef9948')
    assert rsp.status == '401 UNAUTHORIZED'

def test_Register_user_end_point():
    """Test Register_user_end_point"""
    client = app.test_client()
    rsp = client.post('/auth/register',data=user)
    assert rsp.status == '200 OK'

def test_get_users_endpoint():
    """Test the /users end point"""
    client = app.test_client()
    rsp = client.get('/users')
    assert rsp.status == '401 UNAUTHORIZED'

def test_get_one_users_endpoint():
    """Test the /users/****** end point"""
    client = app.test_client()
    rsp = client.get('/users/098c6e4a-f358-4122-b65c-073f5f30a4e5')
    assert rsp.status == '401 UNAUTHORIZED'

def test_delete_one_user_endpoint():
    """Test delete the /users/****** end point"""
    client = app.test_client()
    rsp = client.delete('/users/098c6e4a-f358-4122-b65c-073f5f30a4e5')
    assert rsp.status == '401 UNAUTHORIZED'