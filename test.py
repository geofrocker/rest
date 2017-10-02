"""Test for yummy recipe web app"""
from app import app

def test_home_end_point():
    """Test home page"""
    client = app.test_client()
    rsp = client.get('/')
    assert rsp.status == '200 OK'

def test_add_Recipe_end_point():
    """Test add_Recipe_end_point"""
    client = app.test_client()
    rsp = client.post('/recipe/1')
    assert rsp.status == '200 OK'

def test_edit_Recipe_end_point():
    """Test edit_Recipe_end_point"""
    client = app.test_client()
    rsp = client.put('/recipe/1')
    assert rsp.status == '200 OK'

def test_delete_Recipe_end_point():
    """Test edit_Recipe_end_point"""
    client = app.test_client()
    rsp = client.delete('/recipe/1')
    assert rsp.status == '200 OK'

def test_delete_Recipe_end_point():
    """Test edit_Recipe_end_point"""
    client = app.test_client()
    rsp = client.delete('/recipe/1')
    assert rsp.status == '200 OK'

def test_Register_user_end_point():
    """Test Register_user_end_point"""
    client = app.test_client()
    rsp = client.post('/register')
    assert rsp.status == '200 OK'

def test_Authentication_user_end_point():
    """Test Authenticate_user_end_point"""
    client = app.test_client()
    rsp = client.get('/login')
    assert rsp.status == '200 OK'

