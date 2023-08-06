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

"""Masked token prediction module"""
from transformers import AutoTokenizer, AutoModelForMaskedLM, BertTokenizer, BertForMaskedLM
from transformers import pipeline
import torch
import pandas as pd
from ..config import paths


class MaskFillModel:
    """Fills masked token."""

    def __init__(self, model_name='marathi-bert-v2', gpu_enabled: bool = False):
        self.model_name = model_name
        if model_name not in list(paths["mask_fill"].keys()):
            self.model_route = model_name  # some another model trying to load
            print(f"[warning] the given model '{model_name}' is incompatible.")
        else:
            # user provide model_name that is compatible -> load that model
            # user does not provide key -> load default model
            self.model_route = paths["mask_fill"][model_name]

        self.gpu_enabled = gpu_enabled
        self.device = 1 if (self.gpu_enabled and torch.cuda.is_available()) else -1

        print(f"trying to load '{model_name}' model...")
        if model_name == "marathi-bert-v2":
            self.tokenizer = BertTokenizer.from_pretrained(self.model_route)
            self.model = BertForMaskedLM.from_pretrained(self.model_route)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_route)
            self.model = AutoModelForMaskedLM.from_pretrained(self.model_route)
        print("model loaded!")

        self.generator = pipeline(
            task="fill-mask",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )

    def predict_mask(self, text: str, details: str = "minimum", as_dict: bool = False):
        """Predicts a string for the masked token.

        Args:
            text (str): An input text
            details (str, optional): (minimum, medium, all) - Represents the detailedness
            of the result to be returned.
            as_dict (bool, optional): Used to define the print type. Defaults to False.

        Returns:
            pandas DataFrame: Returns a pandas dataframe
        """
        if text.find(self.tokenizer.mask_token) == -1:
            print("The mask token not set properly.")
            return None
        predictions = pd.DataFrame(self.generator(text))
        predictions['token_str'] = predictions['token_str'].apply(
            lambda word: word.replace(" ", ""))

        if details == 'minimum':
            custom_predict = predictions[['token_str', 'sequence']]

        if details == "medium":
            custom_predict = predictions[['token_str', 'score', 'sequence']]

        if details == "all":
            custom_predict = predictions

        if as_dict:
            return custom_predict.to_dict('records')
        return custom_predict

    def list_models(self):
        """Lists all models supported for masked token prediction."""
        print(" mask_fill models: ")
        for model in paths['mask_fill']:
            print("\t", model, ": ", paths['mask_fill'][model])
        for task in set(paths) - {'mask_fill'}:
            print("\n", task, "models: ")
            for model in paths[task]:
                print("\t", model, ": ", paths[task][model])
