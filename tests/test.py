"""rest api/ test.py"""
from app import app

def test_home_end_point():
    """Test home page"""
    client = app.test_client()
    rsp = client.get('/')
    assert rsp.status == '200 OK'

def test_one_recipe_end_point():
    """Test one recipe"""
    client = app.test_client()
    rsp = client.get('/181c3c3bf-1ed2-4a10-bd40-c808baef9948')
    assert rsp.status == '401 UNAUTHORIZED'

def test_add_Recipe_end_point():
    """Test add_Recipe_end_point"""
    client = app.test_client()
    rsp = client.post('/')
    assert rsp.status == '401 UNAUTHORIZED'

def test_edit_Recipe_end_point():
    """Test edit_Recipe_end_point"""
    client = app.test_client()
    rsp = client.put('/181c3c3bf-1ed2-4a10-bd40-c808baef9948')
    assert rsp.status == '401 UNAUTHORIZED'

def test_delete_Recipe_end_point():
    """Test delete_Recipe_end_point"""
    client = app.test_client()
    rsp = client.delete('/181c3c3bf-1ed2-4a10-bd40-c808baef9948')
    assert rsp.status == '401 UNAUTHORIZED'

def test_Register_user_end_point():
    """Test Register_user_end_point"""
    client = app.test_client()
    user={'id':'5xxxxx', 'name':'Geofrey', 'username':'geom', 'email':'geom@gmail.com', 'password':'12345'}
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