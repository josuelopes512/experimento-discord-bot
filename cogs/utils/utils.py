import os
import uuid
import requests
import mimetypes

def get_extension(content_type):
    data = mimetypes.guess_all_extensions(content_type)
    if type(data) == list:
        return data[-1]
    return data

def get_image(url):
    res = requests.get(url, stream=True)
    image_type = res.headers.get('Content-Type')
    
    filename = uuid.uuid4().hex
    extension = get_extension(image_type)
    
    name_file = f"{filename}{extension}"
    return name_file, res.raw.read() if res.status_code == 200 else None

def save_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
