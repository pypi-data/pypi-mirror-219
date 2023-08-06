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

"""Text preprocessing module"""
import re
from importlib_resources import files
from mahaNLP.tokenizer import Tokenize

class Preprocess:
    """Provides functions for url, stopwords, nondevnagairi script removal."""
    stopwords = []

    def __init__(self):
        if not Preprocess.stopwords:
            lines = files('mahaNLP.preprocess').joinpath(
                'marathi_stopwords.txt').read_text(encoding="utf8").split('\n')
            for line in lines:
                Preprocess.stopwords.append(line.strip())

    def remove_url(self, text):
        """Removes url from the text

        Args:
            text (str): An input text

        Returns:
            str: output text after url discardment
        """
        return re.sub(r"http\S+", "", text)

    def remove_stopwords(self, text):
        """Removes stopwords from the text

        Args:
            text (str): An input text

        Returns:
            str: output text after stopwords discardment
        """
        newlist = []
        tokens = Tokenize()
        textlist = tokens.word_tokenize(text, False)
        for word in textlist:
            if word not in Preprocess.stopwords:
                newlist.append(word)
        return newlist

    def remove_nondevnagari(self, line, en_num = 1):
        """Removes nondevnagari script from text.

        Args:
            line (str): An input text
            en_num (int, optional): Option to retain english numericals. Defaults to 1.
        """
        line = [i for i in line]
        chars = ' क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र '\
            ' ल व र्‍ श ष स ह क़ ख़ ग़ ऩ ड़ ढ़ ऱ य़ ळ ऴ फ़ ज़ ॹ ॺ ॻ ॼ ॾ ॿ ् ऄ अ आ '\
            ' इ ई उ ऊ ॶ ॷ ऋ ॠ ऌ ॡ ॲ ॕ ा ि ी ु ू ॖ ॗ ृ ॄ ॢ ॣ ऍ ऎ ए ऐ ऑ ऒ ओ औ ॵ ॳ '\
            ' ॴ ॅ ॆ े ै ॉ ॊ ो ौ ॏ ऺ ऻ ॎ ॐ ँ ऀ ं ॱ ः ॑ ॒ ॓ ॔ ऽ ॽ , . ० '\
            ' १ २ ३ ४ ५ ६ ७ ८ ९ ₹ । ॥ | ॰ '
        en_nums = '''0123456789'''
        i = 0
        while i < len(line):
            if en_num == 1:
                if ((line[i] not in chars) and (line[i] not in en_nums)):
                    del line[i]
                    i -= 1
                i += 1
            elif en_num == 0:
                if line[i] not in chars:
                    del line[i]
                    i -= 1
                i += 1
            else:
                print("Please pass the correct argument.")
                print(" 1 for retaining English numbers")
                print(" 0 for not retaining English numbers")
                break
        if len(line) == 0:
            print("")
        else:
            if line[0] == " ":
                del line[0]
            if line[len(line)-1] == " ":
                del line[len(line)-1]
            print("".join(line))
