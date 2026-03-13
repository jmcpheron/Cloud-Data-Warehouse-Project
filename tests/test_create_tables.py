"""Tests for create_tables.py — verifies drop/create execute all queries and commit."""

from create_tables import create_tables, drop_tables
from sql_queries import create_table_queries, drop_table_queries


def test_drop_tables_executes_all_queries(mock_cursor, mock_conn):
    drop_tables(mock_cursor, mock_conn)

    assert mock_cursor.execute.call_count == len(drop_table_queries)
    for query in drop_table_queries:
        mock_cursor.execute.assert_any_call(query)

    assert mock_conn.commit.call_count == len(drop_table_queries)


def test_create_tables_executes_all_queries(mock_cursor, mock_conn):
    create_tables(mock_cursor, mock_conn)

    assert mock_cursor.execute.call_count == len(create_table_queries)
    for query in create_table_queries:
        mock_cursor.execute.assert_any_call(query)

    assert mock_conn.commit.call_count == len(create_table_queries)
