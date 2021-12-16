"""
This module implements second query of type A specified in assignment
"""

__author__ = "NAME NAME"
__contact__ = "XLOGIN00@stud.fit.vutbr.cz"
__date__ = "DD-MM-YYYY"

from typing import *
from matplotlib import pyplot as plt
from cassandra.cluster import Cluster
import logging
from tqdm import tqdm
import pandas as pd

class Task_A2:
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
        self.__session.execute("""
            USE {};
        """.format(keyspace))


    def __create_csv(self, filename: str = "A2.csv") -> None:
        """
        Method creates csv dataset for second query of type A
        using data from cassandra db

        Args:
            filename (str): filename of csv dataset, defaultly "A2.csv"
        """

        # check if csv file already exists, in this case get data from file
        try:
            self.__df = pd.read_csv(filename)
            return
        except Exception:
            pass

        infected = self.__session.execute(
            """
            SELECT * FROM infected
            """
        )
        df = pd.DataFrame(list(infected))
        df = df.dropna()
        self.__df = df.fillna(0)
        self.__df.to_csv(filename, sep=",")


    def plot_graph(self, filename: str = "A2.png") -> None:
        """
        Method creates graph according to assignment using dataset
        created by create_csv method

        Args:
            filename (str): name of png file into which graph will be saved,
                defaultly "A2.png"
        """

        # create dataset first

        self.__create_csv()
        self.__df.boxplot(column=['age'], by="region_code", rot=-45)
        plt.suptitle('')
        plt.title("Age of infected people by region NUTS code")
        plt.savefig(filename)
        plt.clf()
