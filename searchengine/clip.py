import requests
import os
import base64


class Clip:

    def download_image_from_url(self, image_url):
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content

    def encode_image_to_base64(self, image_content):
        encoded_string = base64.b64encode(image_content).decode('utf-8')
        return encoded_string


    def text_embeding(self, input):
        
        url = "https://infer.roboflow.com/clip/embed_text"
        params = {
            "api_key": os.environ.get("API_KEY")
        }
        data = {
            "clip_version_id": "ViT-B-16",
            "text": input
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, params=params, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['embeddings'][0]

    def image_embeding(self, input):
        image_content = self.download_image_from_url(input)
        encoded_image = self.encode_image_to_base64(image_content)
        url = "https://infer.roboflow.com/clip/embed_image"
        params = {
            "api_key": os.environ.get("API_KEY")
        }
        data = {
            "clip_version_id": "ViT-B-16",
            "image": [
                {
                    "type": "base64",
                    "value": encoded_image
                }
            ]
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url=url, params=params, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['embeddings'][0]