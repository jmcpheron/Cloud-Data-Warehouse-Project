"""Tests for etl.py — verifies staging load and insert execute all queries and commit."""

from etl import insert_tables, load_staging_tables
from sql_queries import copy_table_queries, insert_table_queries


def test_load_staging_tables_executes_all_queries(mock_cursor, mock_conn):
    load_staging_tables(mock_cursor, mock_conn)

    assert mock_cursor.execute.call_count == len(copy_table_queries)
    for query in copy_table_queries:
        mock_cursor.execute.assert_any_call(query)

    assert mock_conn.commit.call_count == len(copy_table_queries)


def test_insert_tables_executes_all_queries(mock_cursor, mock_conn):
    insert_tables(mock_cursor, mock_conn)

    assert mock_cursor.execute.call_count == len(insert_table_queries)
    for query in insert_table_queries:
        mock_cursor.execute.assert_any_call(query)

    assert mock_conn.commit.call_count == len(insert_table_queries)
