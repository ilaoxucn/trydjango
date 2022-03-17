import requests
import os
from django.core.files import File

endpoint = os.environ.get('FACE_SAAS_URL')
face_saas_token = os.environ.get('FACE_SAAS_TOKEN')

def analyze_pic_via_facesaas(file_obj : File=None):
    print('inside service')
    data = {}
    if endpoint is None:
        return data
    if face_saas_token is None:
        return data
    if file_obj is None:
        return data

    with file_obj.open('rb') as f:
        headers = {
            'Authorization':f'Token {face_saas_token}'
        }
        res = requests.post(endpoint,files={'img':f},headers=headers)
        if res.status_code in range(200,299):
            result = res.json()
            return result

