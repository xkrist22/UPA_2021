"""
This module implements first query of type A specified in assignment
"""

__author__ = "NAME NAME"
__contact__ = "XLOGIN00@stud.fit.vutbr.cz"
__date__ = "DD-MM-YYYY"

from enum import IntEnum
from typing import *
from cassandra.cluster import Cluster
import logging
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

class Task_A1:
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



    def __create_csv(self, filename: str = "A1.csv") -> None:
        """
        Method creates csv dataset for first query of type A
        using data from cassandra db

        Args:
            filename (str): filename of csv dataset, defaultly "A1.csv"
        """

        # check if csv file already exists, in this case get data from file
        try:
            self.__df = pd.read_csv(filename)
            return
        except Exception:
            pass

        # select dates of infected - for each day there is one date per one infected
        infected = self.__session.execute("""
            SELECT date FROM infected;
        """)
        # cast date to datetime type, strip days to get only months and aggregate dataframe to format (month, number of infected) 
        infected = pd.DataFrame(list(infected), columns=["date"])
        infected["date"] = infected["date"].apply(lambda x: pd.to_datetime(str(x), format="%Y-%m-%d", errors="coerce"))
        infected = infected.dropna()
        infected["date"] = infected["date"].dt.strftime("%Y-%m")
        infected["infected"] = 1
        infected = infected.groupby(infected["date"]).aggregate({"infected": "sum"})

        # select dates of cured - for each day there is one date per one cured
        cured = self.__session.execute("""
            SELECT date FROM cured;
        """)
        # cast date to datetime type, strip days to get only months and aggregate dataframe to format (month, number of cured) 
        cured = pd.DataFrame(list(cured), columns=["date"])
        cured["date"] = cured["date"].apply(lambda x: pd.to_datetime(str(x), format="%Y-%m-%d", errors="coerce"))
        cured = cured.dropna()
        cured["date"] = cured["date"].dt.strftime("%Y-%m")
        cured["cured"] = 1
        cured = cured.groupby(cured["date"]).aggregate({"cured": "sum"})

        
        # select number of people accept for hospitalization per day
        hospitalized = self.__session.execute("""
            SELECT date, num_of_first_record FROM hospitalized;
        """)
        # cast date to datetime type, strip days to get only months and aggregate dataframe to format (month, number of first records) 
        hospitalized = pd.DataFrame(list(hospitalized), columns=["date", "hospitalized"])
        hospitalized["hospitalized"] = hospitalized["hospitalized"].apply(lambda x: pd.to_numeric(int(x), errors="coerce"))
        hospitalized["date"] = hospitalized["date"].apply(lambda x: pd.to_datetime(str(x), format="%Y-%m-%d", errors="coerce"))
        hospitalized = hospitalized.dropna()
        hospitalized["date"] = hospitalized["date"].dt.strftime("%Y-%m")
        hospitalized = hospitalized.groupby(hospitalized["date"]).aggregate({"hospitalized": "sum"})

        # select number of people accept for tests per day
        tested = self.__session.execute("""
            SELECT date, daily_tested_region FROM tested;
        """)
        # cast date to datetime type, strip days to get only months and aggregate dataframe to format (month, number of tested) 
        tested = pd.DataFrame(list(tested), columns=["date", "tested"])
        tested["tested"] = tested["tested"].apply(lambda x: pd.to_numeric(int(x), errors="coerce"))
        tested["date"] = tested["date"].apply(lambda x: pd.to_datetime(str(x), format="%Y-%m-%d", errors="coerce"))
        tested = tested.dropna()
        tested["date"] = tested["date"].dt.strftime("%Y-%m")
        tested = tested.groupby(tested["date"]).aggregate({"tested": "sum"})

        # merge data about infected, cured, hospitalized and tested numbers to one dataframe
        df = pd.merge(infected, cured, on="date", how="outer")
        df = pd.merge(df, hospitalized, on="date", how="outer")
        df = pd.merge(df, tested, on="date", how="outer")

        self.__df = df.fillna(0)
        self.__df.to_csv(filename, sep=",")


    def plot_graph(self, filename: str = "A1.png") -> None:
        """
        Method creates graph according to assignment using dataset
        created by create_csv method

        Args:
            filename (str): name of png file into which graph will be saved,
                defaultly "A1.png"
        """

        # create dataset first
        self.__create_csv()

        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(self.__df["date"], self.__df["infected"])
        axs[0, 0].set_title('Infected')
        axs[0, 0].tick_params('x', labelrotation=-45)
        axs[0, 1].plot(self.__df["date"], self.__df["infected"])
        axs[0, 1].set_title('Cured')
        axs[0, 1].tick_params('x', labelrotation=-45)
        axs[1, 0].plot(self.__df["date"], self.__df["cured"])
        axs[1, 0].set_title('Hospitalized')
        axs[1, 0].tick_params('x', labelrotation=-45)
        axs[1, 1].plot(self.__df["date"], self.__df["hospitalized"])
        axs[1, 1].set_title('Tested')
        axs[1, 1].tick_params('x', labelrotation=-45)

        for ax in axs.flat:
            ax.set(xlabel='', ylabel='Count')

        fig.tight_layout()
        plt.savefig(filename)
        plt.clf()


if __name__ == "__main__":
    # establish connection with default values
    a1 = Task_A1("localhost", 9042, "covid")
    a1.plot_graph()
