"""rest api/ test.py"""
password = '12345'
user={'id':'5xxxxx', 'name':'Geofrey', 'username':'geom', 'email':'geom@gmail.com', 'password':password}

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM4NDM5NGYyLTcxZWYtNDZhOS1iOGQ1LWE5MWI4Yjk4MmMwZiIsImV4cCI6MTUwNzIyNzM2OX0.6fllx-QfcQmgkWg3ly-C9_w5SrJWWcMTkto1n5sEVS4'
headers = {'Authorization': 'Basic eyJ0eXAiOiJKV1QiLCJhb',
                        'Content-Type': 'application/json',
                        'x-access-token' : token
                        }
from app import app
def test_home_end_point():
    """Test home page"""
    client = app.test_client()
    rsp = client.get('/')
    assert rsp.status == '200 OK'

def test_one_recipe_end_point():
    """Test one recipe"""
    client = app.test_client()
    rsp = client.get('/181c3c3bf-1ed2-4a10-bd40-c808baef9948',headers=headers)
    assert rsp.status == '200 OK'

def test_add_Recipe_end_point():
    """Test add_Recipe_end_point"""
    client = app.test_client()
    rsp = client.post('/recipe')
    assert rsp.status == '200 OK'

def test_edit_Recipe_end_point():
    """Test edit_Recipe_end_point"""
    client = app.test_client()
    rsp = client.put('/recipe/1')
    assert rsp.status == '200 OK'

def test_delete_Recipe_end_point():
    """Test delete_Recipe_end_point"""
    client = app.test_client()
    rsp = client.delete('/recipe/1')
    assert rsp.status == '200 OK'

def test_Register_user_end_point():
    """Test Register_user_end_point"""
    client = app.test_client()
    rsp = client.post('/auth/register',data=user)
    assert rsp.status == '200 OK'

def test_Authentication_user_end_point():
    """Test Authenticate_user_end_point"""
    client = app.test_client()
    rsp = client.get('/auth/login',)
    assert rsp.status == '401 UNAUTHORIZED'

def test_get_users_endpoint():
    """Test the /users end point"""
    client = app.test_client()
    rsp = client.get('/users/1')
    assert rsp.status == '200 OK'

def test_get_one_users_endpoint():
    """Test the /user/****** end point"""
    client = app.test_client()
    rsp = client.get('/user/098c6e4a-f358-4122-b65c-073f5f30a4e5')
    assert rsp.status == '200 OK'

def test_delete_one_user_endpoint():
    """Test delete the /user/****** end point"""
    client = app.test_client()
    rsp = client.delete('/users/1')
    assert rsp.status == '200 OK'