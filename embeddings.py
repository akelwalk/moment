from transformers import pipeline
from sentence_transformers import SentenceTransformer

class Embeddings():
    def __init__(self):
        self.classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=None)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_emotions(self, text):
        result = self.classifier(text)
        # print(result)   
        # print(result[0][0]["label"])
        return result[0] # it's wrapped in an extra list
    
    def get_vector_embedding(self, text):
        embedding = self.model.encode(text) # type numpy.ndarray
        return embedding
