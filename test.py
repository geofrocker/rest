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
    rsp = client.get('/recipe')
    assert rsp.status == '200 OK'

