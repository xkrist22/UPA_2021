"""
This module implements class containing methods for downloading, caching
and parsing dataset. Dataset is specified by URL from which it can be
downloaded and by type (one of json or csv). File caching is optional and
can be turned on by filling up filename. 
"""

__author__ = "Jiří Křištof"
__contact__ = "xkrist22@stud.fit.vutbr.cz"
__date__ = "06-10-2021"

from typing import *
from json import loads as read_json
from requests import get


class Downloader:
    __SUPPORTED_TYPES = ["json", "csv"]

    @classmethod
    def get_supported_types(cls) -> List[str]:
        """
        Getter of supported dataset types.

        Returns:
            List[str]: list containing all supported types
        """

        return cls.__SUPPORTED_TYPES

    @classmethod
    def get_data(cls, src: str, type: str, filename: str = None) -> Union[list, dict]:
        """
        Method for accessing datasets.

        Method download dataset or read it from existing file. If given file
        does not exists, method create the file and save dataset into it. 

        Parameters:
            src (str): URL from which dataset should be downloaded
            type (str): type of the dataset (must be one of SUPPORTED_TYPES)
            filename (str): name of file where dataset should be cached
        
        Raises:
            AttributeError: raised if dataset format is not supported
        
        Returns:
            Union[list, dict]: parsed dataset in form of (nested) dicts and/or lists
        """

        # check if given type is supported
        if type not in Downloader.__SUPPORTED_TYPES:
            raise AttributeError("Unsupported type {} of the dataset".format(type))

        # if no filename is given, just download dataset and parse it
        if filename is None:
            data = cls.__download_dataset(src)

        else:
            # try to open file and read data from it
            try:
                file = open(filename, "r")
                data = file.read()

            # if reading is unsuccesfull (non-existing file, ...)
            except Exception:
                data = cls.__download_dataset(src)
                file = open(filename, "w")
                file.write(data)

        # return dataset in form of List/Dict
        return cls.__parse_dataset(data, type)

    @classmethod
    def __download_dataset(cls, src: str) -> str:
        """
        Method for downloading dataset from given source url.

        Parameters:
            src (str): URL from which dataset will be downloaded
        """

        r = get(src, allow_redirects=True)
        return r.text

    @classmethod
    def __parse_dataset(cls, data: str, type: str) -> Union[list, dict]:
        """
        Method parse datasets.

        Method calls imported parsers and returns parsed datasets.

        Parameters:
            data (str): dataset in form of string
            type (str): type of dataset, must be one of SUPPORTED_TYPES
        
        Returns:
            Union[list, dict]: dataset in form of (nested) lists/dicts
        """

        if type == "json":
            return read_json(data)
        elif type == "csv":
            # conversion must be used due to csv package 
            return list(cls.read_csv(data))

    @classmethod
    def read_csv(cls, data: str, delimiter: str = ",") -> List[List[str]]:
        """
        Method for parsing csv datasets

        Parameters:
            data (str): comma separated values string
            delimiter (str): used delimiter, defaultly comma
        
        Returns:
            List[List[str]]: returns list of list of str, first level list are rows, 
            nested lists are columns, str are values
        """

        rows = data.splitlines()
        data = [row.replace('"', '').split(",") for row in rows]
        return data
