def test_get_message_no_records(client):
    response = client.get('/api/v1/messages/1')
    response_data = response.get_json()

    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert 'Message with id 1 not found' in response_data['message']


def test_get_message(client, sample_data):
    response = client.get('/api/v1/messages/1')
    response_data = response.get_json()

    expected_data = {
        'id': 1,
        'msg_counter': 1,
        'msg_text': 'Message 1'
    }

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data'] == expected_data


def test_get_message_second_time(client, sample_data):
    response = client.get('/api/v1/messages/1')
    response = client.get('/api/v1/messages/1')
    response_data = response.get_json()

    expected_data = {
        'id': 1,
        'msg_counter': 2,
        'msg_text': 'Message 1'
    }

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data'] == expected_data


def test_create_message(client, token, message):
    response = client.post('/api/v1/messages', 
                           json=message,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()

    expected_data = {
        'id': 1,
        'msg_counter': 0,
        'msg_text': message['msg_text']
    }

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data'] == expected_data
 

def test_create_message_invalid_content_type(client, token, message):
    response = client.post('/api/v1/messages', 
                           data=message,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()

    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    msg = 'Content type must be application/json'
    assert msg in response_data['message']


def test_create_message_missing_token(client, message):
    response = client.post('/api/v1/messages', 
                           json=message)
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    msg = 'Missing token, please login or register'
    assert msg in response_data['message']


def test_update_message_counter_zero(client, sample_data, token, message):
    response = client.get('/api/v1/messages/1')
    response = client.get('/api/v1/messages/1')
    response_data = response.get_json()

    assert response_data['data']['msg_counter'] == 2

    response = client.put('/api/v1/messages/1', 
                           json=message,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()

    expected_data = {
        'id': 1,
        'msg_counter': 0,
        'msg_text': message['msg_text']
    }

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data'] == expected_data


def test_update_message_invalid_content_type(client, sample_data, token, message):
    response = client.put('/api/v1/messages/1', 
                           data=message,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()

    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    msg = 'Content type must be application/json'
    assert msg in response_data['message']


def test_update_message_invalid_missing_token(client, sample_data, message):
    response = client.put('/api/v1/messages/1', 
                           data=message)
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    msg = 'Missing token, please login or register'
    assert msg in response_data['message']


def test_delete_message(client, sample_data, token):
    response = client.delete('/api/v1/messages/1',
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data'] == 'Message with id 1 has been deleted'


def test_delete_message_missing_token(client, sample_data):
    response = client.delete('/api/v1/messages/1')
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    msg = 'Missing token, please login or register'
    assert msg in response_data['message']


def test_delete_message_wrong_token(client, sample_data):
    response = client.delete('/api/v1/messages/1',
                             headers={
                             'Authorization': f'Bearer wrong_token'
                             })
    response_data = response.get_json()

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    msg = 'Invalid token, please login or register'
    assert msg in response_data['message']
