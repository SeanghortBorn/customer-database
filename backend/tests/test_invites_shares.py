import pytest




def test_invite_and_accept_and_register_flow(client):
    # register owner
    res = client.post('/api/auth/register', json={'email': 'owner@example.com', 'password': 'pw', 'name': 'Owner'})
    assert res.status_code == 200

    # login
    res = client.post('/api/auth/token', data={'username': 'owner@example.com', 'password': 'pw'})
    assert res.status_code == 200
    token = res.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # create invite
    res = client.post('/api/invites/', params={'email': 'invitee@example.com', 'role': 'editor'}, headers=headers)
    assert res.status_code == 200
    token = res.json()['token']

    # accept invite (creates placeholder user)
    res = client.get(f'/api/invites/accept?token={token}')
    assert res.status_code == 200
    assert res.json().get('email') == 'invitee@example.com'

    # register the invited user (set password)
    res = client.post('/api/auth/register', json={'email': 'invitee@example.com', 'password': 'newpw', 'name': 'Invitee'}, params={'invite_token': token})
    assert res.status_code == 200

    # login as invitee
    res = client.post('/api/auth/token', data={'username': 'invitee@example.com', 'password': 'newpw'})
    assert res.status_code == 200


def test_share_link_and_view_count(client):
    # register user + create a property
    res = client.post('/api/auth/register', json={'email': 'u2@example.com', 'password': 'pw', 'name': 'User2'})
    assert res.status_code == 200
    res = client.post('/api/auth/token', data={'username': 'u2@example.com', 'password': 'pw'})
    token = res.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # create property
    res = client.post('/api/properties/', json={'name': 'Test Prop'}, headers=headers)
    assert res.status_code == 200
    prop_id = res.json()['id']

    # create link share with max_views=2
    res = client.post('/api/shares/link', params={'resource_type': 'property', 'resource_id': prop_id, 'max_views': 2}, headers=headers)
    assert res.status_code == 200
    token = res.json()['token']

    # resolve link twice (should succeed)
    res = client.get(f'/s/{token}')
    assert res.status_code == 200
    res = client.get(f'/s/{token}')
    assert res.status_code == 200
    # third time should 410
    res = client.get(f'/s/{token}')
    assert res.status_code == 410
