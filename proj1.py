"""
This implements script for downloading dataset about covid-19 disease and
load data into cassandra nosql column database running on given ip and port
"""

__author__ = ["Jiří Křištof", "Petr Češka"]
__contact__ = ["xkrist22@stud.fit.vutbr.cz", "xceska05@stud.fit.vutbr.cz"]
__date__ = "23-10-2021"

from typing import *
from src.downloader import Downloader
from cassandra.cluster import Cluster
from traceback import print_stack


class Proj1:
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
        
        print("* Connecting to cassandra db server on {}:{}".format(ip, port))
        
        self.keyspace = keyspace
        self.downloader = Downloader()
        
        self.cluster = Cluster([ip], port=port)
        self.session = self.cluster.connect()
        self.create_db_structure()


    def create_db_structure(self):
        """
        Method creates tables for storing data with given structure
        described in docs
        """


    def load_data_into_db(self, data_sources: List[(str, str)]):
        """
        Method adds data into pre-created tables

        Parameters:
            data_sources (List[str]): list of tuples, where
                the first elem is url of dataset and second is
                name of table into which data will be saved
        """

    
    def destroy_data(self):
        """
        Method drops whole keyspace
        """
        
        confirm = str(input("* Are you sure you want to remove ALL data [Y/N]:"))
        if confirm.lower() == "y":
            self.session.execute("DROP KEYSPACE IF EXISTS {}".format(self.keyspace))
            print("* Keyspace {} removed".format(self.keyspace))
        else:
            print("* Data not affected")


if __name__ == "__main__":
    #TODO
    data_sources = []

    db = Proj1()
    db.load_data_into_db(data_sources)
