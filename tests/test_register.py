import requests
import json
import sys

def register_user():
    register_data = {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'password123',
        'role': 'Healthcare Staff'
    }
    
    try:
        print('Registering test user...')
        response = requests.post('http://localhost:8000/auth/register', json=register_data)
        print(f'Register Response Status: {response.status_code}')
        if response.status_code == 200:
            print('User registered successfully')
            print(f'Response: {response.text[:200]}')
            return True
        else:
            print(f'Registration failed: {response.text}')
            return False
    except Exception as e:
        print(f'Error: {str(e)}')
        return False

if __name__ == '__main__':
    success = register_user()
    sys.exit(0 if success else 1)