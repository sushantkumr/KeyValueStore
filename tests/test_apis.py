def test_set_pair(client):
    payload = {
        "key": "xyz_6",
        "value": "value_6"
    }

    response = client.post(
            '/set',
            data=payload,
        )
    assert response.status_code == 200

def test_get_pair(client):
    response = client.get('/get/xyz_1')
    assert response.status_code == 200

def test_search_pair_prefix(client):
    response = client.get('/search?prefix=xyz')
    assert response.status_code == 200

def test_search_pair_suffix(client):
    response = client.get('/search?suffix=-1')
    assert response.status_code == 200
