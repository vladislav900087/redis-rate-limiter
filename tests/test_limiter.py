

def test_read_root(client):

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_ping(client):

    response = client.get('/ping')

    assert response.status_code == 200

    assert response.json() == {'message': 'pong'}