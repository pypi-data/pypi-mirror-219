# MIT License

# Copyright (c) 2022 L3Cube Pune

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Sentence Similarity Analyzer module"""
from sentence_transformers import SentenceTransformer, util
from ..config import paths

class SimilarityModel:
    """Provides sentence embeddings and sentence similarity score functionalities."""

    def __init__(self, model_name = 'marathi-sentence-similarity-sbert', gpu_enabled:bool = False):
        self.model_name = model_name
        if model_name not in list(paths["similarity"].keys()):
            self.model_route = model_name  # some another model trying to load
            print(f"[warning] the given model '{model_name}' is incompatible.")
        else:
            # user provide model_name that is compatible -> load that model
            # user does not provide key -> load default model
            self.model_route = paths["similarity"][model_name]

        self.model = SentenceTransformer(self.model_route)

    def embed_sentences(self,sentences):
        """Embeds the input sentence

        Args:
            sentences (str): An input text

        Returns:
            list: array of embeddings
        """
        sentence_embeddings = self.model.encode(sentences)
        return sentence_embeddings

    def get_similarity_score(self, source_sentence, sentences, as_dict: bool = False):
        """Checks the similarity of a sentence with respect to array of sentences

        Args:
            source_sentence (str): An input text
            sentences (list): List of input sentences to be compared with the source sentence
            as_dict (bool, optional): Used to define the print type. Defaults to False.

        Returns:
            list: returns a list of similarity scores.
        """
        embeddings1 = self.embed_sentences(source_sentence)
        embeddings2 = self.embed_sentences(sentences)
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        result_np_array = cosine_scores.numpy()[0]

        if as_dict:
            dictionary = {}
            if isinstance(sentences, str):
                sentences = [sentences]
            for i, sentence in enumerate(sentences):
                dictionary[sentence] =  result_np_array[i]
            return dictionary
        return result_np_array

    def list_models(self):
        """Lists all sentence similarity models."""
        print(" similarity models: ")
        for model in paths['similarity']:
            print("\t",model, ": ", paths['similarity'][model])
        for task in set(paths) - {'similarity'}:
            print("\n",task,"models: ")
            for model in paths[task]:
                print("\t",model, ": ", paths[task][model])
