import openai
import faiss
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self, dim=1536):
        self.dim = dim
        self.index_file = os.path.join('aida','store', 'aida.index')
        self.metadata_file = os.path.join('aida','store', 'metadata.pkl')
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            self.load_index()
        else:
            self.index = faiss.IndexFlatL2(self.dim)  # Using L2 distance for similarity search
            self.metadata = []

    def load_index(self):
        """Load the FAISS index and metadata if they exist."""
        self.index = faiss.read_index(self.index_file)
        with open(self.metadata_file, 'rb') as f:
            self.metadata = pickle.load(f)

    def save_index(self):
        """Save the FAISS index and metadata to disk."""
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)

    def get_openai_embedding(self, text):
        """Generate an embedding for the text using OpenAI's API."""
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        return np.array(embedding, dtype='float32')

    def update_vector_store(self, text):
        """Add new text to the vector store."""
        vector = self.get_openai_embedding(text)
        self.index.add(np.array([vector]))
        self.metadata.append({'text': text})
        self.save_index()

    def query_vector_store(self, query, top_k=10):
        """Retrieve the most relevant texts from the vector store based on the query."""
        query_vector = self.get_openai_embedding(query)
        distances, indices = self.index.search(np.array([query_vector]), top_k)
        results = [self.metadata[i] for i in indices[0]]
        return results

# store = VectorStore()

# with open(os.path.join('store', 'context.txt')) as file:
#     text = file.read()
# store.update_vector_store(text)

