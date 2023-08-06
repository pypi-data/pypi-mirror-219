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

"""Tokenize module"""

class Tokenize:
    """Provides sentence and word tokenization functionalties."""

    def __init__(self,lang='mr'):
        self.lang = lang

    def sentence_tokenize_mr(self, txt):
        """Internal function for Marathi sentence tokenization, not meant for programmer's usage

        Args:
            txt (str): An input text consisting of multiple sentences.

        Returns:
            list: list of sentences.
        """
        punc_for_sentence_end = '''.!?'''
        sentences = []
        string = ""
        for i in txt:
            if i == "\n":
                continue
            if i not in punc_for_sentence_end:
                string += i
            else:
                string += i
                sentences.append(string)
                string = ""

        return sentences

    def sentence_tokenize(self, txt):
        """Tokenizes sentences from paragraph or set of sentences.

        Args:
            txt (str): An input text consisting of multiple sentences.

        Returns:
            list: list of sentences.
        """
        if self.lang == 'mr':
            return self.sentence_tokenize_mr(txt)


    def word_tokenize_mr(self, txt, punctuation):
        """Internal function for Marathi word tokenization, not meant for programmer's usage

        Args:
            txt (str): An input text.
            punctuation (bool): Decides whether to tokenize punctuation marks

        Returns:
            list: list of words.
        """
        punc = '''\\!()-[]{};:'",<>./?@#$%^&*_~'''
        if punctuation:
            string = ""
            tokens = []
            for ele in txt:
                if ele in punc:
                    if string:
                        tokens.append(string)
                        string = ""
                    tokens.append(ele)
                elif ele == " ":
                    if string:
                        tokens.append(string)
                        string = ""
                else:
                    string += ele
            if string:
                tokens.append(string)
                string = ""
            return tokens

        for ele in txt:
            if ele in punc:
                txt = txt.replace(ele, " ")
        result = txt.split()
        return result

    def word_tokenize(self, line, punctuation=True):
        """Tokenizes words from sentences.

        Args:
            line (str): An input text.
            punctuation (bool, optional): Decides whether to tokenize punctuation marks. 
            Defaults to True.

        Returns:
            list: list of words
        """
        if self.lang == 'mr':
            result = self.word_tokenize_mr(line, punctuation)
            return result
