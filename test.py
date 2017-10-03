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
    rsp = client.get('/recipe/1')
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
    rsp = client.post('/auth/register')
    assert rsp.status == '200 OK'

def test_Authentication_user_end_point():
    """Test Authenticate_user_end_point"""
    client = app.test_client()
    rsp = client.get('/auth/login')
    assert rsp.status == '200 OK'
    
