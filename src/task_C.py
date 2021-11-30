"""
This module implements creation of dataset specified in assignment
"""

__author__ = "NAME NAME"
__contact__ = "XLOGIN00@stud.fit.vutbr.cz"
__date__ = "DD-MM-YYYY"

from typing import *
from cassandra.cluster import Cluster
import logging
from tqdm import tqdm


class Task_C:
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


    def create_dataset(self, filename: str = "C.csv") -> None:
        """
        Method creates dataset according to assignment

        Args:
            filename (str): name of dataset file into which dataset
                will be saved, defaultly "C.csv"
        """

        #TODO