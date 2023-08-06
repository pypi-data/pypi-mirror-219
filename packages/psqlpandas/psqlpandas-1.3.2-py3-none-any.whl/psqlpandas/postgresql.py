from typing import List, Dict, Tuple, Any
import logging

import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras as pgex
from sqlalchemy import create_engine


class PostgresqlDatabaseConnector:
    def __init__(
        self, dbname: str, user: str, host: str, port: str, password: str
    ) -> None:
        self._conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname,
        )
        self._sqlalchemy_conn = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        )

    def __del__(self) -> None:
        self._conn.close()
        self._sqlalchemy_conn.dispose()

    @staticmethod
    def execute_values(cursor, query, tuples):
        return pgex.execute_values(cursor, query, tuples)

    def read(self, query: str, params: Tuple[Any] | None = None) -> List[Tuple[str]]:
        """
        Reads values from database.

        NOTE: around 3x faster than self.read_df

        Args:
            query (str): select query to be executed
            params (Tuple[Any], optional): bind parameters to pass to the query. Defaults to None.

        Returns:
            List[Tuple[str]]: list of rows retrieved
        """
        cur = self._conn.cursor()
        params = params if params is not None else tuple()

        try:
            cur.execute(query, params)
            data = cur.fetchall()
        except Exception as e:
            logging.error(f"Error while reading query: {query}")
            logging.error(e)
            cur.close()
            raise
        else:
            cur.close()
            return data

    def read_df(
        self,
        query: str,
        parse_dates: List[str] | str | None = None,
        uppercase_colnames: bool = False,
        params: Tuple[Any] | None = None,
    ) -> pd.DataFrame:
        """
        Reads values from database directly into pandas dataframe

        NOTE: generally slower than self.read. But can be usefult for automatic casting of types (including dates).

        Args:
            query (str): select query to be executed
            parse_dates (List[str] | str | None, optional): columns to be parsed at dates. Defaults to None.
            uppercase_colnames (bool, optional): whether to return uppercase colnames. Defaults to False.
            params (Tuple[Any], optional): bind parameters to pass to the query. Defaults to None.

        Returns:
            pd.DataFrame: dataframe of data retrieved
        """
        params = params if params is not None else tuple()
        try:
            data = pd.read_sql_query(
                query, con=self._sqlalchemy_conn, parse_dates=parse_dates, params=params
            )
            if uppercase_colnames:
                data.columns = data.columns.str.upper()
            return data
        except Exception as e:
            logging.error(f"Error while reading query: {query}")
            logging.error(e)
            raise

    def execute_sql_query(self, query, row=None):
        cur = self._conn.cursor()

        try:
            if row is None:
                cur.execute(query)
            else:
                cur.execute(query, row)
            self._conn.commit()
            cur.close()
            return True
        except Exception as e:
            logging.error(f"Error while executing query: {query}")
            logging.error(e)
            cur.close()
            raise

    def execute_sql_query_values(self, query: str, tuples: Tuple[Any]):
        cur = self._conn.cursor()

        try:
            self.execute_values(cur, query, tuples)
            self._conn.commit()
            cur.close()
            return True
        except Exception as e:
            logging.error(f"Error while executing query: {query}")
            logging.error(e)
            cur.close()
            raise

    def update_db_row(
        self,
        df_dict: Dict[str, object],
        tablename: str,
        sql_where_condition: str | None = None,
    ) -> bool:

        # If you have more than one columns to update
        if len(df_dict.keys()) > 1:
            sql = "UPDATE {} SET ({}) = ({}) ".format(
                tablename,
                ",".join([column for column in df_dict.keys()]),
                ",".join(
                    [
                        f"'{element}'" if element not in [None, []] else "NULL"
                        for element in df_dict.values()
                    ]
                ),
            )
        # If you have only 1 column to modify need to configure a different query
        elif len(df_dict.keys()) == 1:
            sql = f"UPDATE {tablename} SET {list(df_dict.keys())[0]} = {list(df_dict.values())[0]} "
        else:
            raise ValueError(
                "Impossible to generate the update query since data are empty"
            )

        if sql_where_condition is not None:
            sql += sql_where_condition

        return self.execute_sql_query(sql)

    def delete_db_row(
        self,
        tablename: str,
        sql_where_condition: str,
        direct_delete: bool = False,
        update_field: str = "available",
    ) -> bool:
        """
        Delete a database data composing a SQL String with tablename and row id you want to remove

        Args:
            tablename (str): Name of the table
            sql_where_condition (str): SQL Where condition to attach to the query (it's important because you want to delete only a single row).
                Impossible to use the delete without a where setting: for policy and safety purpose.
            direct_delete (bool): If you want to direct delete a row, or just want to update a flag
            update_field (str): Flag field for the deletion (available field column)

        Returns:
            bool: query execution result (True or False)
        """
        # Delete directly the row or bulk of rows
        if direct_delete:
            sql = f"DELETE FROM {tablename} "
        # Just update the flag: available to False
        else:
            sql = f"UPDATE {tablename} SET {update_field} = False "

        # Compose the where condition (it's mandatory to avoid unwanted deletion)
        sql += sql_where_condition

        return self.execute_sql_query(sql)

    def insert_from_df(
        self, tablename: str, df: pd.DataFrame, replace: bool = False
    ) -> bool:
        """
        Inserts data from a pandas dataframe to postgres db.

        Args:
            tablename (str): target tablename
            df (pd.DataFrame): dataframe with data
            replace (bool, optional): whether to replace or not already present data. Defaults to False.

        Returns:
            bool: True if successful without errors
        """

        # duplicate the object because it's required to manipulate some columns
        df_columns = list(set(df.columns) - {"id"})

        # Setting null (and inf) values to None for postgres
        tuples = [
            tuple(x)
            for x in df.astype(object)
            .where(pd.notnull(df) & ~df.isin([np.inf, -np.inf]), None)[df_columns]
            .to_numpy()
        ]

        insertsql = "INSERT INTO {} ({}) VALUES %s".format(
            tablename, ",".join(df_columns)
        )

        # Update if there are data already
        if replace:
            # Query from https://wiki.postgresql.org/wiki/Retrieve_primary_key_columns
            primary_keys_sql = (
                f"SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND "
                f"a.attnum = ANY(i.indkey) WHERE i.indrelid = '{tablename}'::regclass AND i.indisprimary;"
            )
            primary_keys = list(self.read_df(primary_keys_sql))
            columns_to_update = [x for x in df_columns if x not in primary_keys]
            insertsql = (
                insertsql
                + " ON CONFLICT ON CONSTRAINT "
                + tablename
                + "_pkey DO UPDATE SET ("
                + ",".join([column for column in columns_to_update])
                + ") = ("
                + ",".join(["EXCLUDED." + column for column in columns_to_update])
                + ")"
            )

        return self.execute_sql_query_values(insertsql, tuples)
