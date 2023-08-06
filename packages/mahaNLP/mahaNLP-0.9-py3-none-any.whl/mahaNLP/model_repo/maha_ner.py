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

"""Named Entity Recognition module"""
from transformers import BertTokenizerFast, BertForTokenClassification, TokenClassificationPipeline
import torch
import pandas as pd
from ..config import paths

class NERModel:
    """Entity recognition along with the scores."""

    def __init__(self, model_name='marathi-ner',gpu_enabled:bool = False):
        self.model_name = model_name
        if model_name not in list(paths["tagger"].keys()):
            self.model_route = model_name  # some another model trying to load
            print(f"[warning] the given model '{model_name}' is incompatible.")
        else:
            # user provide model_name that is compatible -> load that model
            # user does not provide key -> load default model
            self.model_route = paths["tagger"][model_name]


        self.gpu_enabled = gpu_enabled
        self.device = 1 if (self.gpu_enabled and torch.cuda.is_available()) else -1

        print(f"trying to load '{model_name}' model...")
        self.ner_tokenizer = BertTokenizerFast.from_pretrained(self.model_route)
        self.pretrained_ner_model = BertForTokenClassification.from_pretrained(self.model_route)
        print("model loaded!")

        self.pipeline = TokenClassificationPipeline(
            task='marathi-ner',
            model=self.pretrained_ner_model,
            tokenizer=self.ner_tokenizer,
            framework="pt",
            aggregation_strategy='first',
            device=self.device,
        )

    def get_token_labels(self, text, details: str = "minimum",as_dict:bool = False):
        """Entity recognition of every token

        Args:
            text (str): An input text
            details (str, optional): (minimum, medium, all) - Defines the level of details
            to get from the prediction. Defaults to "minimum".
            as_dict (bool, optional): Used to define the print type. Defaults to False.

        Returns:
            list: lisr of entity tokens and scores
        """
        labels = pd.DataFrame(self.pipeline(text))

        labels['word'] = labels['word'].apply(lambda arr:list(arr.split(" ")))
        labels = labels.explode('word',ignore_index=True)
        columns = ['word','entity_group','score','start','end']

        if details == 'minimum':
            predicts = labels[columns[:2]]

        if details == "medium":
            predicts = labels[columns[:3]]

        if details == "all":
            predicts = labels[columns]

        if as_dict:
            return predicts.to_dict('records')
        return predicts

    def get_tokens(self,text):
        """Get only entity tokens

        Args:
            text (str): An input text

        Returns
            str: String of token entities
        """
        predictions = self.pipeline(text)

        token_labels  = ""
        for token in predictions:
            subwords = list(token['word'].strip().split(" "))
            for _ in subwords:
                token_labels  = token_labels + (" "  + token['entity_group'])

        token_labels = token_labels.lstrip()
        return token_labels


    def list_models(self):
        """Lists all models supported for named entity recognition."""
        print(" tagger models: ")
        for model in paths['tagger']:
            print("\t",model, ": ", paths['tagger'][model])
        for task in set(paths) - {'tagger'}:
            print("\n",task,"models: ")
            for model in paths[task]:
                print("\t",model, ": ", paths[task][model])
