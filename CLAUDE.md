# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AWS Redshift cloud data warehouse for a music streaming app (Sparkify). An ETL pipeline extracts song and event log data from S3, loads it into Redshift staging tables, then transforms it into a star schema for analytics.

## Commands

```bash
# Step 1: Create/reset all tables (drops existing tables first)
python create_tables.py

# Step 2: Run ETL pipeline (S3 → staging → star schema)
python etl.py
```

Requires a running Redshift cluster and valid `dwh.cfg` configuration. The Jupyter notebook (`Jupyter Notebook for Testing.ipynb`) handles cluster provisioning via AWS SDK and connectivity testing.

## Architecture

**Three-file pipeline:**
- `sql_queries.py` — All SQL statements (DDL, COPY, INSERT). Single source of truth for schema and transformations. Other scripts import query lists from here.
- `create_tables.py` — Drops and recreates all tables by iterating over `drop_table_queries` and `create_table_queries` from `sql_queries.py`.
- `etl.py` — Runs the ETL by iterating over `copy_table_queries` (S3 → staging) then `insert_table_queries` (staging → star schema).

**Data flow:** S3 → `staging_events` + `staging_songs` (via Redshift COPY) → star schema tables

**Star schema tables:**
- Fact: `songplays` (joins staging tables on song title + artist name)
- Dimensions: `users`, `songs`, `artists`, `time`

## Configuration

`dwh.cfg` contains AWS credentials, Redshift cluster connection details, IAM role ARN, and S3 paths. Sensitive values (KEY, SECRET, HOST, ARN) must be filled in before running.

## Dependencies

- `psycopg2` — PostgreSQL/Redshift driver
- `configparser` — Config file parsing (stdlib)
