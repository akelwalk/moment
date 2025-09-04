from transformers import pipeline
from sentence_transformers import SentenceTransformer
import json5

class Embeddings():
    def __init__(self):
        self.classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1) # only returning the highest matched emotion
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_emotions(self, text):
        result = self.classifier(text)
        return result[0][0]["label"] # it's wrapped in an extra list
    
    def get_vector_embedding(self, text):
        embedding = self.model.encode(text) # type numpy.ndarray
        return embedding.tobytes()

