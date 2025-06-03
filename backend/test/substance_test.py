import requests

url = 'http://localhost:5000'


def add_substance():
    data = {
        'substance_name': 'air',
        'quantity': ''
    }
    r = requests.post(f'{url}/add_substance', json=data)
    print(r.status_code)
    print(r.text)
    print(requests.get(f'{url}/get_substances').text)


def update_substance():
    data = {
        'substance_id': '1',
        'substance_name': 'air-2',
        'quantity': '10ml'
    }
    r = requests.post(f'{url}/update_substance', json=data)
    print(r.status_code)
    print(r.text)
    print(requests.get(f'{url}/get_substances').text)


def delete_substance():
    data = {
        'substance_id': '1'
    }
    r = requests.post(f'{url}/delete_substance', json=data)
    print(r.status_code)
    print(r.text)
    print(requests.get(f'{url}/get_substances').text)


if __name__ == '__main__':
    add_substance()
    update_substance()
    delete_substance()