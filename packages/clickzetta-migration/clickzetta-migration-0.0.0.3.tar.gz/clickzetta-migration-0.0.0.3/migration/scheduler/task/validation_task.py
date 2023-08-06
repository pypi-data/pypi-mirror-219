import logging
from datetime import datetime

from migration.base.status import TaskType, TaskStatus
from migration.connector.destination.base import Destination
from migration.connector.source import Source
from migration.connector.source.enum import Column
from migration.scheduler.task import Task
from migration.util import migration_tasks_status

logger = logging.getLogger(__name__)
NUMBER_TYPE = ['BIGINT', 'DECIMAL', 'DOUBLE', 'FLOAT', 'INT', 'SMALLINT', 'TINYINT']
LEFT_BRACKET = '('


class ValidationTask(Task):
    def __init__(self, name: str, task_type: TaskType, source: Source, destination: Destination, *args, **kwargs):
        super().__init__(name, task_type, *args, **kwargs)
        self.source = source
        self.destination = destination

    def run(self):
        try:
            if not self.check_count():
                return self
            if not self.check_number_type_statistics():
                return self
            self.status = TaskStatus.COMPLETED
        except BaseException as e:
            self.status = TaskStatus.FAILED
            return self
        self.end_time = datetime.now()
        migration_tasks_status.update_task_status(self.destination, self)
        logger.info(f"ValidationTask {self.name} finished running, status: {self.status.value}")
        return self

    def check_count(self):
        sql = f"select count(*) from {self.name}"
        source_count = self.source.execute_sql(sql)
        destination_count = self.destination.execute_sql(sql)
        if source_count != destination_count:
            self.status = TaskStatus.FAILED
            self.end_time = datetime.now()
            migration_tasks_status.update_task_status(self.destination, self)
            logger.error(
                f"ValidationTask {self.name} failed to run, error: count not equal, retry times: {self.retry_times}")
            return False
        return True

    def check_number_type_statistics(self):
        type_mapping = self.source.type_mapping()
        table_columns = self.source.get_table_columns(self.name.split('.')[0], self.name.split('.')[1])
        for column in table_columns:
            if self.is_number_type(column, type_mapping):
                sql = f"select min({column.name}), max({column.name}), avg({column.name}) from {self.name}"
                source_result = self.source.execute_sql(sql)
                destination_result = self.destination.execute_sql(sql)
                if source_result != destination_result:
                    self.status = TaskStatus.FAILED
                    self.end_time = datetime.now()
                    migration_tasks_status.update_task_status(self.destination, self)
                    logger.error(
                        f'ValidationTask {self.name} failed to run, error: number type statistics not equal, retry times: {self.retry_times}')
                    return False
        return True

    def check_string_type_statistics(self):
        pass

    def check_top_n(self):
        pass

    def is_number_type(self, column: Column, type_mapping: dict) -> bool:
        if LEFT_BRACKET in column.type:
            column_type = column.type.split(LEFT_BRACKET)[0]
            return type_mapping.get(column_type, column_type) in NUMBER_TYPE

        return type_mapping.get(column.type, column.type) in NUMBER_TYPE
