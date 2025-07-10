import faiss
import numpy as np


class VectorDB:
    def __init__(self):
        _DIMENSION = 1536
        self.index = faiss.IndexFlatL2(_DIMENSION)

    async def save_vector(self, vectors):
        """
        Saves the vector in the database with the provided key.

        Args:

        """
        # vectors = np.array(vectors).astype('float32')
        # faiss.normalize_L2(vectors)
        self.index.add(vectors)
        pass

    async def get_similar_data(self, query_vector, threshold=0.2, k=10):
        """
        Searches for matching vectors based on a query vector.

        Args:
            threshold:
            query (str): Query string.

        Returns:
            str: Matched documents' content concatenated.
        """
        _normalized_vector = np.array(query_vector).astype("float32").reshape(1, -1)
        # faiss.normalize_L2(_normalized_vector)
        vector_string = ""
        distances, indices = self.index.search(_normalized_vector, k)
        for val in indices[0]:
            if val != -1 and distances[0][val] > threshold:
                vector_string += str(self.index.reconstruct(int(val))) + "\n\n"
        return vector_string
