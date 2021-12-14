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
import logging
from tqdm import tqdm


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
        self.__downloader = Downloader()

        self.__cluster = Cluster([ip], port=port)
        self.__session = self.__cluster.connect()


    def create_db_structure(self):
        """
        Method creates tables for storing data with given structure
        described in docs
        """

        print("* Creating keyspace {}".format(self.keyspace))
        self.__session.execute("""
            CREATE KEYSPACE IF NOT EXISTS covid 
            WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
        """)

        self.__session.execute("""
            USE covid;
        """)

        print("* Creating tables")
        self.__session.execute("""
            CREATE TABLE IF NOT EXISTS infected (
                date date,
                age int,
                gender text,
                region_code text,
                district_code text,
                foreign_infection_country text,

                PRIMARY KEY (
                    region_code,
                    gender,
                    age
                )
            );
        """)

        self.__session.execute("""
            CREATE TABLE IF NOT EXISTS cured (
                date date,
                age int,
                gender text,
                region_code text,
                district_code text,

                PRIMARY KEY (
                    region_code,
                    gender,
                    age
                )
            );
        """)

        self.__session.execute("""
            CREATE TABLE IF NOT EXISTS died_covid (
                date date,
                age int,
                gender text,
                region_code text,
                district_code text,

                PRIMARY KEY (
                    region_code,
                    gender,
                    age
                )
            );
        """)

        self.__session.execute("""
            CREATE TABLE IF NOT EXISTS hospitalized (
                date date,
                num_of_first_record int,
                cumulative_first_record int,
                hospitalized_num int,
                no_symptom int,
                light_symptom int,
                medium_symptom int,
                hard_symptom int,
                intensive_cure_num int,
                oxygen_support int,

                PRIMARY KEY (
                    date
                )
            );
        """)

        self.__session.execute("""
            CREATE TABLE IF NOT EXISTS tested (
                date date,
                region_code text,
                district_code text,
                daily_tested_district int,
                cumulative_tested_district int,
                daily_tested_region int,
                cumulative_tested_region int,

                PRIMARY KEY (
                    region_code
                )
            );
        """)

        self.__session.execute("""
            CREATE TABLE IF NOT EXISTS vaccinated (
                date date,
                vaccine_name text,
                region_code text,
                age_group text,
                first_vaccine_num int,
                second_vaccine_num int,
                total_vaccine_num int,

                PRIMARY KEY (
                    region_code,
                    age_group
                )
            );
        """)

        self.__session.execute("""
            CREATE TABLE IF NOT EXISTS died (
                age_group text,
                date_from date,
                date_to date,
                year int,
                week int,
                value int,
                PRIMARY KEY (
                    age_group,
                    year,
                    week
                )
            );
        """)


    def parse_infected(self, dataset):
        """
        Method adds data into pre-created table 'infected'

        Parameters:
            dataset (Union[list, dict]): parsed dataset in form of (nested) dicts and/or lists
        """

        # remove rows where primary key element is not filled
        dataset = [row for row in dataset if row[2] != '' and row[3] != '' and row[4] != '']
        
        for row in tqdm(dataset[1:]):  # first row is table header
            try:
                self.__session.execute(
                    """
                    INSERT INTO infected (date, age, gender, region_code, district_code, foreign_infection_country)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (row[1], int(row[2]), row[3], row[4], row[5], row[7])
                )
            except Exception:
                tqdm.write("* Row {} cannot be added into table \"infected\", see file \"insert.log\" for more information".format(row))
                logging.exception("Exception raised while adding into table \"infected\"\n\trow: {}".format(row))
                continue


    def parse_cured(self, dataset):
        """
        Method adds data into pre-created table 'cured'

        Parameters:
            dataset (Union[list, dict]): parsed dataset in form of (nested) dicts and/or lists
        """

        # remove rows where primary key element is not filled
        dataset = [row for row in dataset if row[2] != '' and row[3] != '' and row[4] != '']

        for row in tqdm(dataset[1:]):  # first row is table header
            try:
                self.__session.execute(
                    """
                    INSERT INTO cured (date, age, gender, region_code, district_code)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (row[1], int(row[2]), row[3], row[4], row[5])
                )
            except Exception:
                tqdm.write("* Row {} cannot be added into table \"cured\", see file \"insert.log\" for more information".format(row))
                logging.exception("Exception raised while adding into table \"cured\"\n\trow: {}".format(row))
                continue


    def parse_died_covid(self, dataset):
        """
        Method adds data into pre-created table 'died_covid'

        Parameters:
            dataset (Union[list, dict]): parsed dataset in form of (nested) dicts and/or lists
        """

        # remove rows where primary key element is not filled
        dataset = [row for row in dataset if row[2] != '' and row[3] != '' and row[4] != '']

        for row in tqdm(dataset[1:]):  # first row is table header
            try:
                self.__session.execute(
                    """
                    INSERT INTO died_covid (date, age, gender, region_code, district_code)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (row[1], int(row[2]), row[3], row[4], row[5])
                )
            except Exception:
                tqdm.write("* Row {} cannot be added into table \"died_covid\", see file \"insert.log\" for more information".format(row))
                logging.exception("Exception raised while adding into table \"died_covid\"\n\trow: {}".format(row))
                continue


    def parse_hospitalized(self, dataset):
        """
        Method adds data into pre-created table 'hospitalized'

        Parameters:
            dataset (Union[list, dict]): parsed dataset in form of (nested) dicts and/or lists
        """

        # remove rows where primary key element is not filled
        dataset = [row for row in dataset if row[1] != '']

        for row in tqdm(dataset[1:]):  # first row is table header
            try:
                self.__session.execute(
                    """
                    INSERT INTO hospitalized (
                    date,
                    num_of_first_record,
                    cumulative_first_record,
                    hospitalized_num,
                    no_symptom,
                    light_symptom,
                    medium_symptom,
                    hard_symptom,
                    intensive_cure_num,
                    oxygen_support
                        )  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (row[1], int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8]),
                     int(row[9]), int(row[10]))
                )
            except Exception:
                tqdm.write("* Row {} cannot be added into table \"hospitalized\", see file \"insert.log\" for more information".format(row))
                logging.exception("Exception raised while adding into table \"hospitalized\"\n\trow: {}".format(row))
                continue


    def parse_tested(self, dataset):
        """
        Method adds data into pre-created table 'tested'

        Parameters:
            dataset (Union[list, dict]): parsed dataset in form of (nested) dicts and/or lists
        """

        # remove rows where primary key element is not filled
        dataset = [row for row in dataset if row[2] != '']

        for row in tqdm(dataset[1:]):  # first row is table header
            try:
                self.__session.execute(
                    """
                    INSERT INTO tested (
                    date,
                    region_code,
                    district_code,
                    daily_tested_district,
                    cumulative_tested_district,
                    daily_tested_region,
                    cumulative_tested_region
                        )  VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (row[1], row[2], row[3], int(row[4]), int(row[5]), int(row[6]), int(row[7]))
                )
            except Exception:
                tqdm.write("* Row {} cannot be added into table \"tested\", see file \"insert.log\" for more information".format(row))
                logging.exception("Exception raised while adding into table \"tested\"\n\trow: {}".format(row))
                continue


    def parse_vaccinated(self, dataset):
        """
        Method adds data into pre-created table 'vaccinated'

        Parameters:
            dataset (Union[list, dict]): parsed dataset in form of (nested) dicts and/or lists
        """

        # remove rows where primary key element is not filled
        dataset = [row for row in dataset if row[3] != '' and row[5] != '']

        for row in tqdm(dataset[1:]):  # first row is table header
            try:
                self.__session.execute(
                    """
                    INSERT INTO vaccinated (
                        date,
                        vaccine_name,
                        region_code,
                        age_group,
                        first_vaccine_num,
                        second_vaccine_num,
                        total_vaccine_num
                        )  VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (row[1], row[2], row[3], row[5], int(row[6]), int(row[7]), int(row[8]))
                )
            except Exception:
                tqdm.write("* Row {} cannot be added into table \"vaccinated\", see file \"insert.log\" for more information".format(row))
                logging.exception("Exception raised while adding into table \"vaccinated\"\n\trow: {}".format(row))
                continue


    def parse_died(self, dataset):
        """
        Method adds data into pre-created table 'died'

        Parameters:
            dataset (Union[list, dict]): parsed dataset in form of (nested) dicts and/or lists
        """

        # remove rows where primary key element is not filled
        dataset = [row for row in dataset if row[12] != '' and row[7] != '' and row[8] != '']

        for row in tqdm(dataset[1:]):  # first row is table header
            try:
                if row[12] != "celkem":
                    self.__session.execute(
                        """
                        INSERT INTO died (age_group, date_from, date_to, year, week, value)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (row[12], row[10], row[11], int(row[7]), int(row[8]), int(row[1]))
                    )
            except Exception:
                tqdm.write("* Row {} cannot be added into table \"died\", see file \"insert.log\" for more information".format(row))
                logging.exception("Exception raised while adding into table \"died\"\n\trow: {}".format(row))
                continue


    def load_data_into_db(self, data_sources: List[Tuple[str, str]]):
        """
        Method calls special methods, that adds data into pre-created tables, for each dataset

        Parameters:
            data_sources (List[str]): list of tuples, where
                the first elem is url of dataset and second is
                name of table into which data will be saved
        """

        dl = Downloader()
 
        print("* Note that ^C stop adding data into any table and start adding into next table")
        for link in data_sources:
            # get dataset from given url link[0]
            dataset = dl.get_data(link[0], 'csv', link[1] + '_cache.csv')
            print("* Loading data from dataset {} into table {}".format(link[0], link[1]))
            # for each dataset at url link[0] add data from it into table specified in link[1]
            try:
                eval('self.parse_' + link[1] + '(dataset)')
            except KeyboardInterrupt:
                print("* Adding into table {} stopped after keyboard interrupt".format(link[1]))


    def destroy_data(self):
        """
        Method drops whole keyspace
        """

        confirm = str(input("* Are you sure you want to remove ALL data [Y/N]:"))
        if confirm.lower() == "y":
            self.__session.execute("""
                DROP KEYSPACE IF EXISTS {}
                """.format(self.keyspace)
                                   )
            print("* Keyspace {} removed".format(self.keyspace))
        else:
            print("* Data not affected")


if __name__ == "__main__":
    logging.basicConfig(filename='insert.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    data_sources = [
        ("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv", "infected"),
        ("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/vyleceni.csv", "cured"),
        ("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv", "died_covid"),
        ("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv", "hospitalized"),
        ("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-testy.csv", "tested"),
        ("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv", "vaccinated"),
        ("https://www.czso.cz/documents/62353418/155512389/130185-21data101921.csv", "died"),
    ]

    db = Proj1()
    db.create_db_structure()
    try:
        db.load_data_into_db(data_sources)
    except KeyboardInterrupt:
        db.destroy_data()
