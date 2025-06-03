import requests

url = 'http://127.0.0.1:5050'


def test_index():
    r = requests.get(f'{url}/')
    print(r.text)


def test_add_device():
    for port in ['COM6', 'COM8']:
        data = {
            'device_nickname': 'test' + port,
            'com_port': port
        }
        r = requests.post(f'{url}/register_device', json=data)
        print(r.text)
        test_index()


def test_remove_device():
    for port in ['COM6', 'COM8']:
        data = {
            'device_nickname': 'test' + port
        }
        r = requests.post(f'{url}/de_register_device', json=data)
        print(r.text)
        test_index()


def test_add_remove():
    test_index()
    test_add_device()
    test_remove_device()


test_add_remove()
