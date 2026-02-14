import pytest


def test_register_and_token_flow(client):
    email = 'testuser@example.com'
    res = client.post('/api/auth/register', json={'email': email, 'password': 'secret', 'name': 'Test'})
    assert res.status_code == 200
    res2 = client.post('/api/auth/token', data={'username': email, 'password': 'secret'})
    assert res2.status_code == 200
    assert 'access_token' in res2.json()
