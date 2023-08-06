from typing import List, Tuple, Dict, Any
import logging

import pandas as pd
import psqlpandas.postgresql as psql


def drop_table_query(tablename: str) -> str:
    """
    Builds the drop table query.

    Args:
        tablename (str): Table name

    Returns:
        str: drop table query
    """
    return f"DROP TABLE IF EXISTS {tablename}"


def create_table_query(
    tablename: str,
    columns_specs: List[Tuple[str, str]],
    primary_keys: List[str],
) -> str:
    """
    Builds craete table query.

    Args:
        tablename (str): table name
        columns_specs (List[Tuple[str, str]]): spcification of the columns, that is, list of all column names and related types
        primary_keys (List[str]): list of columns to be used as primary keys

    Returns:
        str: the create table query.
    """

    sql = f"CREATE TABLE IF NOT EXISTS {tablename}"
    sql_cols = ", ".join([f"{col} {coltype}" for col, coltype in columns_specs])
    primary_key_sql = f"PRIMARY KEY ({', '.join(primary_keys)})"
    sql = f"{sql} ({sql_cols}, {primary_key_sql})"
    logging.debug(f"Create table query: {sql}")

    return sql


def initialize_table_checks(table_info: Dict[str, Any]) -> bool:
    """
    Checks whether all mandatory keys for the information about tables are present in
    the dictionary passed.

    Args:
        table_info (Dict[str, Any]): dictionary containing the table specifications

    Returns:
        bool: False if any of the mandatory key is missing
    """
    mandatory_keys = ["tablename", "columns", "primary_key", "drop_if_exists"]
    for mk in mandatory_keys:
        if mk not in table_info:
            logging.error(f"Missing mandatory key {mk} in table infos")
            return False
    return True


def initialize_table(
    table_info: Dict[str, Any],
    db_connector: psql.PostgresqlDatabaseConnector,
    data: pd.DataFrame,
) -> bool:
    """
    Initialize a db table.

    Performs the following steps:
    1. drop table if requested (and if it exisits)
    2. create table
    3. upload provided data

    NOTE: if table is not requested to be dropped, input data are inserted in the table
        replacing old values with the same key

    Args:
        table_info (Dict[str, object]): dictionary containing the table specifications
        db_connector (psql.PostgresqlDatabaseConnector): connector to the db
        data (pd.DataFrame): data
    """

    if not initialize_table_checks(table_info):
        return False

    tablename = table_info["tablename"]

    # Drop table
    if table_info["drop_if_exists"]:
        db_connector.execute_sql_query(drop_table_query(tablename))
        logging.debug(f"Dropped table {tablename}")

    # Create table
    db_connector.execute_sql_query(
        create_table_query(
            tablename,
            columns_specs=table_info["columns"].items(),
            primary_keys=table_info["primary_key"]["cols"],
        )
    )

    # Upload data
    db_connector.insert_from_df(
        tablename, data, replace=not table_info["drop_if_exists"]
    )

    return True
