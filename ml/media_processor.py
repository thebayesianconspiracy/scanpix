import numpy as np
from transformers import CLIPProcessor, CLIPModel
from helpers import get_image_from_url


class ClipModel:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    def get_embedding(self, input, type):
        if type == "image":
            input_dict = {"images": input}
            get_features = self.model.get_image_features
        elif type == "text":
            input_dict = {"text": input}
            get_features = self.model.get_text_features
        else:
            raise ValueError("Input type not recognized!")
        processed_input = self.processor(return_tensors="pt", **input_dict)
        embedding = get_features(**processed_input).tolist()
        embedding /= np.linalg.norm(embedding)
        return embedding.ravel().tolist()


class MediaProcessor():
    def __init__(self):
        self.clip_model = ClipModel()

    def process_image(self, url):
        img = get_image_from_url(url)
        return self.clip_model.get_embedding(img, 'image')

    def process_text(self, text):
        return self.clip_model.get_embedding(text, 'text')
