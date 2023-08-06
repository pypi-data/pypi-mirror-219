import requests
import json

class Scoreosaurus:
    def __init__(self, api_url):
        self.api_url = api_url


    def save_score(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(self.api_url + "/score", files=files)
        
        if response.status_code != 200:
            raise Exception(f"File upload failed with status {response.status_code}")
        
        result = response.json()

        # Przyjmujemy, że odpowiedź API zawiera pole 'score', które jest wynikiem w formacie float
        score = float(result.get('score', 0))
        return score



    def upload_file(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(self.api_url + "/upload", files=files)
        
        if response.status_code != 200:
            raise Exception(f"File upload failed with status {response.status_code}")

        return response.json()
