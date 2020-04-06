from .conftest import client

def test_root(client):
    resp = client.get('/')
    assert resp 
