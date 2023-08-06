import logging
import re

import pymysql
import sqlparse

from migration.connector.source.base import Source
from migration.base.exceptions import SourceExecutionError
from migration.connector.source.enum import Column, ClusterInfo
import migration.util.object_storage_util as object_storage_util

logger = logging.getLogger(__name__)


class DorisSource(Source):
    def __init__(self, config: dict, meta_conf_path=None, storage_conf_path=None):
        super().__init__('Doris', config)
        self.connection_params = self.get_connection_params()
        self.meta_conf_path = meta_conf_path
        self.storage_config_path = storage_conf_path

    """
    Doris connection parameters is a dict including following keys:
    1. host: host of Doris
    2. port: port for mysql client, default is 9030
    3. database: database name
    4. user: user name
    5. passwd: password
    """

    def get_connection_params(self):
        assert self.config['fe_servers']
        assert self.config['user']
        assert self.config['password']

        return {
            'host': self.config['fe_servers'][0].split(':')[0],
            'port': int(self.config['fe_servers'][0].split(':')[1]),
            'user': self.config['user'],
            'password': self.config['password']
        }

    def connect(self):
        if self.connection is None:
            self.connection = pymysql.connect(**self.connection_params)
            logger.info(f"Connect to Doris {self.connection_params['host']} successfully")

    def get_database_names(self):
        result = self.execute_sql("show databases")
        return [row[0] for row in result]

    def get_table_names(self, database_name):
        result = self.execute_sql(f"show tables from {database_name}")
        return [row[0] for row in result]

    def get_ddl_sql(self, database_name, table_name):
        return self.execute_sql(f"show create table {database_name}.{table_name}")[0][1]

    def get_table_cluster_info(self, database_name, table_name):
        ddl_sql = self.get_ddl_sql(database_name, table_name)
        cluster_columns = []
        ddl_format_sql = sqlparse.format(ddl_sql, reindent=True, keyword_case='upper')
        match_result = re.match(r'(.*)DISTRIBUTED(.*)BY(.*?)\((.*?)\)(.*)BUCKETS(.*?)(\d+).*', ddl_format_sql, re.S)
        if match_result:
            for cluster_column in match_result.group(4).strip().split(','):
                cluster_columns.append(cluster_column.replace('`', '').strip())
            return ClusterInfo(int(match_result.group(7).strip()), cluster_columns)

        return None

    def get_table_partition_columns(self, database_name, table_name):
        ddl_sql = self.get_ddl_sql(database_name, table_name)
        partition_columns = []
        ddl_format_sql = sqlparse.format(ddl_sql, reindent=True, keyword_case='upper')
        match_result = re.match(r'(.*?)PARTITION(.*?)BY(.*?)\((.*?)\).*', ddl_format_sql, re.S)
        if match_result:
            for partition_column in match_result.group(4).strip().split(','):
                partition_columns.append(partition_column.replace('`', '').strip())
            return partition_columns
        return None

    def get_primary_key(self, database_name, table_name):
        ddl_sql = self.get_ddl_sql(database_name, table_name)
        primary_keys = []
        ddl_format_sql = sqlparse.format(ddl_sql, reindent=True, keyword_case='upper')
        match_result = re.match(r'(.*?)UNIQUE(.*?)KEY(.*?)\((.*?)\).*', ddl_format_sql, re.S)
        if match_result:
            for primary_key in match_result.group(4).strip().split(','):
                primary_keys.append(primary_key.replace('`', '').strip())
            return primary_keys
        return None

    def get_table_columns(self, database_name, table_name) -> list[Column]:
        result = self.execute_sql(f"desc {database_name}.{table_name}")
        table_columns = []
        for row in result:
            table_columns.append(Column(name=row[0], type=row[1].upper(),
                                        is_null=True if row[2].strip() == 'Yes' else False,
                                        default_value=row[4]))
        return table_columns

    def execute_sql(self, sql, bind_params=None):
        try:
            self.connect()
            with self.connection.cursor() as cur:
                cur.execute(sql, bind_params)
                return cur.fetchall()

        except SourceExecutionError as e:
            logger.error(f"Doris connector execute sql {sql} failed, error: {e}")
            raise f"Doris connector execute sql {sql} failed, error: {e}"

    def type_mapping(self):
        return {
            'DATETIME': 'TIMESTAMP',
        }

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            logger.info(f"Close connection to Doris {self.connection_params['host']} successfully")

    def unload_data(self, task):
        file_path = f"{task.project_id}/{task.id}/{task.name.split('.')[1]}/"
        object_storage_conf = object_storage_util.get_object_storage_config(self.storage_config_path)
        predicated = ''
        if hasattr(task, 'transform_partitions'):
            predicated = ' WHERE '
            columns = task.transform_partitions[0]
            values = task.transform_partitions[1]
            if len(columns) != len(values):
                raise BaseException('The length of transform_partitions columns and values is not equal')
            for i in range(len(columns)):
                predicated += f" {columns[i]} = '{values[1]}' and "
            predicated = predicated[:-4]
        unload_sql = f"SELECT * FROM {task.name} {predicated} INTO OUTFILE \"s3://{object_storage_conf['bucket']}/{file_path}\" " \
                     f"FORMAT AS PARQUET" \
                     f"properties(" \
                     f"\"AWS_ENDPOINT\"=\"{object_storage_conf['endpoint']}\"," \
                     f"\"AWS_ACCESS_KEY\"=\"{object_storage_conf['id']}\"," \
                     f"\"AWS_SECRET_KEY\"=\"{object_storage_conf['key']}\"," \
                     f"\"AWS_REGION\"=\"{object_storage_conf['region']}\"," \
                     f")"

        self.execute_sql(unload_sql)
        return [file_path]
