"""
This module implements first custom query
"""

__author__ = "NAME NAME"
__contact__ = "XLOGIN00@stud.fit.vutbr.cz"
__date__ = "DD-MM-YYYY"

from typing import *
from cassandra.cluster import Cluster
import logging
from tqdm import tqdm


class Task_custom1:
    def __init__(self, ip: str = "localhost", port: int = 9042, keyspace: str = "covid"):
        """
        Method initializes connection with casandra db server on given
        ip and port.

        Parameters:
            ip (str): ip address of the cassandra nosql db server, defaultly "localhost"
            port (int): port where cassandra db server is listnening, defaultly 9042
            keyspace (str): name of keyspace for db,  dedfaultly "covid"
        
        Raises:
            cassandra.cluster.NoHostavailable: raised when server is 
                not running on given ip or port
        """

        self.keyspace = keyspace

        # create cassandra db handler
        self.__cluster = Cluster([ip], port=port)
        self.__session = self.__cluster.connect()


    def __create_csv(self, filename: str = "custom1.csv") -> None:
        """
        Method creates csv dataset for first query of type A
        using data from cassandra db

        Args:
            filename (str): filename of csv dataset, defaultly "custom1.csv"
        """

        #TODO


    def plot_graph(self, filename: str = "custom1.png") -> None:
        """
        Method creates graph according to assignment using dataset
        created by create_csv method

        Args:
            filename (str): name of png file into which graph will be saved,
                defaultly "custom1.png"
        """

        # create dataset first
        self.__create_csv()

        #TODO