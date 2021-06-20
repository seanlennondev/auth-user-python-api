# from faker import Faker
import pytest
from httpx import (
    get,
    post,
    delete
)

# fake = Faker('pt-br')

@pytest.fixture(scope='module')
def inputs():
    return {
        'email': fake.email(),
        'password': fake.password()
    }

@pytest.fixture(scope='module')
def new_user():
    return {
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password()
    }

@pytest.fixture(scope='module')
def get_token():
    res = post(
        'http://localhost:5000/api/users/auth',
        json={
            'email': 'sean@gmail.com',
            'password': '12345'
        },
        headers={
            'Content-Type': 'application/json'
        }
    )
    return res.json()['data']

@pytest.fixture(scope='module')
def create_user(new_user):
    res = post('http://localhost:5000/api/users', json=new_user)
    return res.json()

@pytest.fixture(scope='module')
def d_user(get_token):
    return delete('http://localhost:5000/api/users/1', headers={
        'Authorization': f'Bearer {get_token}'
    })

