"""Tests for sql_queries.py — validates SQL structure without a live Redshift cluster."""

import re

from sql_queries import (
    copy_table_queries,
    create_table_queries,
    drop_table_queries,
    insert_table_queries,
)

EXPECTED_TABLES = {"staging_events", "staging_songs", "songplays", "users", "songs", "artists", "time"}


# --- Query list lengths ---


def test_drop_query_count():
    assert len(drop_table_queries) == 7


def test_create_query_count():
    assert len(create_table_queries) == 7


def test_copy_query_count():
    assert len(copy_table_queries) == 2


def test_insert_query_count():
    assert len(insert_table_queries) == 5


# --- DROP queries ---


def test_drop_queries_use_if_exists():
    for query in drop_table_queries:
        assert "IF EXISTS" in query.upper(), f"Missing IF EXISTS: {query[:60]}"


def test_drop_queries_cover_all_tables():
    dropped = set()
    for query in drop_table_queries:
        match = re.search(r"DROP\s+TABLE\s+IF\s+EXISTS\s+(\w+)", query, re.IGNORECASE)
        assert match, f"Could not parse table name from: {query[:60]}"
        dropped.add(match.group(1).lower())
    assert dropped == EXPECTED_TABLES


# --- CREATE queries ---


def test_create_queries_have_primary_key():
    for query in create_table_queries:
        assert "PRIMARY KEY" in query.upper(), f"Missing PRIMARY KEY: {query[:60]}"


def test_create_queries_no_trailing_semicolons():
    for query in create_table_queries:
        assert not query.strip().endswith(";"), f"Trailing semicolon: {query[-30:]}"


def test_create_queries_cover_all_tables():
    created = set()
    for query in create_table_queries:
        match = re.search(r"CREATE\s+TABLE\s+(\w+)", query, re.IGNORECASE)
        assert match, f"Could not parse table name from: {query[:60]}"
        created.add(match.group(1).lower())
    assert created == EXPECTED_TABLES


def test_every_create_has_matching_drop():
    created = set()
    for query in create_table_queries:
        match = re.search(r"CREATE\s+TABLE\s+(\w+)", query, re.IGNORECASE)
        created.add(match.group(1).lower())

    dropped = set()
    for query in drop_table_queries:
        match = re.search(r"DROP\s+TABLE\s+IF\s+EXISTS\s+(\w+)", query, re.IGNORECASE)
        dropped.add(match.group(1).lower())

    assert created == dropped, f"Mismatch — created: {created - dropped}, dropped only: {dropped - created}"


# --- COPY queries ---


def test_copy_queries_contain_credentials():
    for query in copy_table_queries:
        assert "CREDENTIALS" in query.upper(), f"Missing CREDENTIALS: {query[:60]}"


# --- INSERT queries ---


def test_insert_queries_use_select():
    for query in insert_table_queries:
        assert "SELECT" in query.upper(), f"Missing SELECT: {query[:60]}"


# --- Config values loaded ---


def test_config_values_loaded():
    from sql_queries import IAM_ROLE, LOG_DATA, SONG_DATA

    assert LOG_DATA, "LOG_DATA is empty"
    assert SONG_DATA, "SONG_DATA is empty"
    assert IAM_ROLE, "IAM_ROLE is empty"
