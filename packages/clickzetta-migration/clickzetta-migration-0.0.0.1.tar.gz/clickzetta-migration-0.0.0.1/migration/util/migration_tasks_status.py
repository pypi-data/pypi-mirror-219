import logging

from migration.connector.destination.base import Destination
from migration.scheduler.task.base_task import Task
from migration.base.status import Status

STATUS_SCHEMA = "cz_migration"
logger = logging.getLogger(__name__)
PK_TABLE_DML_HINT = {'hints': {'cz.sql.allow.insert.table.with.pk': 'true'}}
INCREMENTAL_INDEX = 0


def init_status_table(destination: Destination, project_name: str):
    if destination.name.lower() == "clickzetta":
        destination.execute_sql(f"CREATE SCHEMA IF NOT EXISTS {STATUS_SCHEMA}")

        tables_in_schema = destination.execute_sql(
            f"show tables in  {STATUS_SCHEMA} where table_name like '{project_name}_%'")
        exist_status_tables = [x[1] for x in tables_in_schema]
        exist_status_tables_index = []
        for table in exist_status_tables:
            try:
                exist_status_tables_index.append(int(table.split("_")[-1]))
            except ValueError:
                raise ValueError(f"Table name {table} is not valid")
        exist_status_tables_index.sort()
        table_index = 0 if not exist_status_tables else exist_status_tables_index[-1] + 1
        table_name = f"{STATUS_SCHEMA}.{project_name}_{table_index}"

        ddl = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT NOT NULL,
            task_id STRING NOT NULL,
            task_name STRING NOT NULL,
            prject_id STRING NOT NULL,
            task_status STRING NOT NULL,
            task_type STRING NOT NULL,
            task_start_time TIMESTAMP NOT NULL,
            task_end_time TIMESTAMP,
            PRIMARY KEY (id)
        )
        """
        destination.execute_sql(ddl)
        return f"{project_name}_{table_index}"
    elif destination.name.lower() == "doris":
        destination.execute_sql(f"CREATE DATABASE IF NOT EXISTS {STATUS_SCHEMA}")
        tables_in_schema = destination.execute_sql(
            f"show tables in  {STATUS_SCHEMA} where table_name like '{project_name}_%'")
        exist_status_tables = [x[0] for x in tables_in_schema]
        exist_status_tables_index = []
        for table in exist_status_tables:
            try:
                exist_status_tables_index.append(int(table.split("_")[-1]))
            except ValueError:
                raise ValueError(f"Table name {table} is not valid")
        exist_status_tables_index.sort()
        table_index = 0 if not exist_status_tables else exist_status_tables_index[-1] + 1
        table_name = f"{STATUS_SCHEMA}.{project_name}_{table_index}"
        ddl = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT NOT NULL,
            task_id STRING NOT NULL,
            task_name STRING NOT NULL,
            prject_id STRING NOT NULL,
            task_status STRING NOT NULL,
            task_type STRING NOT NULL,
            task_start_time DATETIME NOT NULL,
            task_end_time DATETIME
        )
        UNIQUE KEY (id)
        DISTRIBUTED BY HASH(id) BUCKETS 6;
        """
        destination.execute_sql(ddl)
        return f"{project_name}_{table_index}"


def update_task_status(destination: Destination, task: Task):
    if destination.name.lower() == "clickzetta":
        destination.execute_sql(
            f"UPDATE {STATUS_SCHEMA}.{task.project_id} SET task_status = '{task.status.value}', task_end_time = cast('{task.end_time}' as timestamp) WHERE id = '{task.status_id}'",
            PK_TABLE_DML_HINT)
    elif destination.name.lower() == "doris":
        destination.execute_sql(
            f"UPDATE {STATUS_SCHEMA}.{task.project_id} SET task_status = '{task.status.value}', task_end_time = cast('{task.end_time}' as datetime) WHERE id = '{task.status_id}'")
    logger.info(f"Updated task {task.id} status to {task.status.value}")


def init_task_status(destination: Destination, task: Task):
    sql = None
    global INCREMENTAL_INDEX
    if destination.name.lower() == "clickzetta":
        sql = f"""
        INSERT INTO {STATUS_SCHEMA}.{task.project_id} (id, task_id, task_name, prject_id, task_status, task_type, task_start_time, task_end_time) 
        values ('{INCREMENTAL_INDEX}','{task.id}', '{task.name}','{task.project_id}','{task.status.value}', '{task.task_type.value}', cast('{task.start_time}' as timestamp), null)
        """
        destination.execute_sql(sql, PK_TABLE_DML_HINT)
    elif destination.name.lower() == "doris":
        sql = f"""
        INSERT INTO {STATUS_SCHEMA}.{task.project_id} (id, task_id, task_name, prject_id, task_status, task_type, task_start_time, task_end_time) 
        values ('{INCREMENTAL_INDEX}','{task.id}', '{task.name}','{task.project_id}','{task.status.value}', '{task.task_type.value}', cast('{task.start_time}' as datetime), null)
        """
        destination.execute_sql(sql)
    task.status_id = INCREMENTAL_INDEX
    INCREMENTAL_INDEX += 1
    logger.info(f"Inited task {task.id} status")
