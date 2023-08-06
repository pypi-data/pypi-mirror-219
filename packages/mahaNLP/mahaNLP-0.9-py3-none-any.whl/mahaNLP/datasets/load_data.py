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

"""Download of Marathi datasets for further desired programme usage."""
import os
import pandas as pd

def checkdir(dataset_name):
    """Internal function to check if required root folders exist and create folders if needed.
      Not meant for programmer's usage.


    Args:
        dataset_name (str): name of the dataset 

    Returns:
        str: returns the path to current working directory of the workspace / the home directory 
    """
    root_path = os.path.expanduser(r'~\.cache/')
    if not os.path.isdir(root_path):
        os.makedirs(os.getcwd()+'/.cache/mahaNLP/'+dataset_name,exist_ok=True)
        return os.getcwd()
    root_path = os.path.expanduser(r'~\.cache/')
    os.chdir(root_path)
    os.makedirs('mahaNLP/'+dataset_name,exist_ok=True)
    return '~'

def download_mahasent():
    """Internal function to download mahaSent datasets.
     Not meant for programmer's usage.

    Returns:
        dict: returns a dictionary of dataframes
    """
    dataset_type = {
        'tweets-train.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3CubeMahaSent%20Dataset/tweets-train.csv',

        'tweets-test.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3CubeMahaSent%20Dataset/tweets-test.csv',

        'tweets-valid.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3CubeMahaSent%20Dataset/tweets-valid.csv',

        'tweets-extra.csv': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3CubeMahaSent%20Dataset/tweets-extra.csv'
    }
    result = {}
    root_path = os.path.expanduser(checkdir('mahaSent'))
    child_path = os.path.expanduser(root_path+'/.cache/mahaNLP/mahaSent')
    os.chdir(child_path)
    for key, value in dataset_type.items():
        dataframe = pd.read_csv(value)
        dataframe.to_csv(key, index=False, encoding='UTF-16')
        result[key.split(".", maxsplit=1)[0]] = dataframe  # add dataframe to an dictionary
    os.chdir(root_path)
    return result

def download_mahaner():
    """Internal function to download mahaNER datasets.
     Not meant for programmer's usage.

    Returns:
        dict: returns a dictionary of dataframes
    """
    iob = {
        'train_iob.txt': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaNER/IOB/train_iob.txt?raw=true',

        'test_iob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3Cube-MahaNER/IOB/test_iob.txt',

        'valid_iob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3Cube-MahaNER/IOB/valid_iob.txt',
    }
    non_iob = {
        'train_noniob.txt': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaNER/NON_IOB/train_noniob.txt?raw=true',

        'test_noniob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3Cube-MahaNER/NON_IOB/test_noniob.txt',

        'valid_noniob.txt': 'https://raw.githubusercontent.com/l3cube-pune/MarathiNLP/'\
        'main/L3Cube-MahaNER/NON_IOB/valid_noniob.txt',
    }
    result = {'iob': {}, 'non_iob': {}}

    root_path = os.path.expanduser(checkdir('mahaNER/IOB'))
    root_path = os.path.expanduser(checkdir('mahaNER/NON_IOB'))

    child_path = os.path.expanduser(root_path+'/.cache/mahaNLP/mahaNER/IOB')
    os.chdir(child_path)
    for key, value in iob.items():
        dataframe = pd.read_csv(value, sep=" ")
        dataframe.to_csv(key, index=False, encoding='UTF-16')
        result['iob'][key.split(".", maxsplit=1)[0]] = dataframe  # add dataframe to an dictionary

    child_path = os.path.expanduser(root_path+'/.cache/mahaNLP/mahaNER/NON_IOB')
    os.chdir(child_path)
    for key, value in non_iob.items():
        dataframe = pd.read_csv(value, sep="\t")
        dataframe.to_csv(key, index=False, encoding='UTF-16', sep="\t")
        result['non_iob'][key.split(".", maxsplit=1)[0]] = dataframe #add dataframe to an dictionary
    os.chdir(root_path)
    return result

def download_mahahate():
    """Internal function to download mahaHate datasets.
     Not meant for programmer's usage.

    Returns:
        dict: returns a dictionary of dataframes
    """
    class_2 = {
        'hate_bin_train.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaHate/2-class/hate_bin_train.xlsx?raw=true',

        'hate_bin_test.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaHate/2-class/hate_bin_test.xlsx?raw=true',

        'hate_bin_valid.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaHate/2-class/hate_bin_valid.xlsx?raw=true',
    }
    class_4 = {
        'hate_train.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaHate/4-class/hate_train.xlsx?raw=true',

        'hate_test.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaHate/4-class/hate_test.xlsx?raw=true',

        'hate_valid.xlsx': 'https://github.com/l3cube-pune/MarathiNLP/'\
        'blob/main/L3Cube-MahaHate/4-class/hate_valid.xlsx?raw=true',
    }
    result = {'2-class': {}, '4-class': {}}

    root_path = os.path.expanduser(checkdir('mahaHate/2-class'))
    root_path = os.path.expanduser(checkdir('mahaHate/4-class'))

    child_path = os.path.expanduser(root_path+'/.cache/mahaNLP/mahaHate/2-class')
    os.chdir(child_path)
    for key, value in class_2.items():
        dataframe = pd.read_excel(value)
        dataframe.to_excel(key, index=False, encoding='UTF-16')
        result['2-class'][key.split(".", maxsplit=1)[0]] = dataframe #add dataframe to an dictionary

    child_path = os.path.expanduser(root_path+'/.cache/mahaNLP/mahaHate/4-class')
    os.chdir(child_path)
    for key, value in class_4.items():
        dataframe = pd.read_excel(value)
        dataframe.to_excel(key, index=False, encoding='UTF-16')
        result['4-class'][key.split(".", maxsplit=1)[0]] = dataframe #add dataframe to an dictionary
    os.chdir(root_path)
    return result


def load_datasets(name):
    """Downloads the mentioned datasets by calling helper funtions.

    Args:
        name (str): name of the dataset

    Returns:
        dict: returns a dictionary of dataframes
    """
    if name == 'mahaSent':
        res_dict = download_mahasent()
        return res_dict
    if name == 'mahaHate':
        res_dict = download_mahahate()
        return res_dict
    if name == 'mahaNER':
        res_dict = download_mahaner()
        return res_dict
    return None
