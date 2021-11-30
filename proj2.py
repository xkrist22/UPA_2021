"""
Implementation of script running queries of second assignment 
"""

__author__ = ["Jiří Křištof", "Petr Češka"]
__contact__ = ["xkrist22@stud.fit.vutbr.cz", "xceska05@stud.fit.vutbr.cz"]
__date__ = "30-11-2021"

from typing import *
from src.task_A1 import Task_A1
from src.task_A2 import Task_A2
from src.task_B import Task_B
from src.task_custom1 import Task_custom1
from src.task_custom2 import Task_custom2
from src.task_C import Task_C


class Proj2:
    def __init__(self, ip: str = "localhost", port: int = 9042, keyspace: str = "covid"):
        """
        Method creates submodules of each assignment

        Parameters:
            ip (str): ip address of the cassandra nosql db server, defaultly "localhost"
            port (int): port where cassandra db server is listnening, defaultly 9042
            keyspace (str): name of keyspace for db,  dedfaultly "covid"
        """

        self.__a1 = Task_A1(ip, port, keyspace)
        self.__a2 = Task_A2(ip, port, keyspace)
        self.__b = Task_B(ip, port, keyspace)
        self.__custom1 = Task_custom1(ip, port, keyspace)
        self.__custom1 = Task_custom2(ip, port, keyspace)
        self.__c = Task_C(ip, port, keyspace)
    

    def run_proj(self) -> None:
        """
        Method runs all submodules to produce results of assignment
        """

        self.__a1.plot_graph()
        self.__a2.plot_graph()
        self.__b.plot_graph()
        self.__custom1.plot_graph()
        self.__custom2.plot_graph()
        self.__c.create_dataset()


if __name__ == "__main__":
    p = Proj2()
    p.run_proj()

