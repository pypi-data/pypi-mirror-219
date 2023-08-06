import os.path
import unittest
import sqlparse
import re

from migration.connector.destination.clickzetta.destination import ClickZettaDestination


class TestUtil(unittest.TestCase):
    def test_sqlparse(self):
        sql = '''
        CREATE TABLE table2
(
    event_day DATE,
    siteid INT DEFAULT '10',
    citycode SMALLINT,
    username VARCHAR(32) DEFAULT '',
    pv BIGINT SUM DEFAULT '0'
)
UNIQUE    KEY (event_day, siteid, citycode, username)
PARTITION BY RANGE(`event_day`)
(
    PARTITION p201706 VALUES LESS THAN ('2017-07-01'),
    PARTITION p201707 VALUES LESS THAN ('2017-08-01'),
    PARTITION p201708 VALUES LESS THAN ('2017-09-01')
)
DISTRIBUTED BY HASH(`siteid`) BUCKETS 10
PROPERTIES("replication_num" = "1");
        '''
        sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        # result = re.match(r'(.*)AGGREGATE(.*)KEY(.*?)\((.*?)\).*', sql, re.S)
        result = re.match(r'(.*)DISTRIBUTED(.*)BY(.*?)\((.*?)\)(.*)BUCKETS(.*?)(\d+).*', sql, re.S)
        # result = re.match(r'(.*?)PARTITION(.*?)BY(.*?)\((.*?)\).*', sql, re.S)
        # result = re.match(r'(.*?)UNIQUE(.*?)KEY(.*?)\((.*?)\).*', sql, re.S)
        for column in result.group(4).strip().split(','):
            print(column.replace('`', '').strip())

        print(result.group(7).strip())
        print('vachar(32)'.upper())

    def test_list_spilt(self):
        class Box:
            def __init__(self, name):
                self.name = name

        boxes_tasks_map = {}
        tasks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        b = [tasks[i:i + 3] for i in range(0, len(tasks), 3)]

        print(b)

    def test_path(self):

        all_tasks = []
        a = ['a1', 'a2', 'a3']
        b = ['b1', 'b2', 'b3']
        c = ['c1', 'c2', 'c3']
        for i in range(3):
            all_tasks.extend((a[i], b[i], c[i]))
        print(all_tasks)

    def test_destination(self):
        PK_TABLE_DML_HINT = {'hints': {'cz.sql.allow.insert.table.with.pk': 'true'}}
        config = {'service': 'poc-ap-shanghai-tencentcloud.api.clickzetta.com', 'username': 'changean', 'workspace': 'quickStart_WS',
                  'password': 'Achangean123!', 'instance': '1fdbc4a7', 'vcluster': 'DEFAULT', "instanceId": 32}
        destination = ClickZettaDestination(config)
        print(destination.execute_sql('show schemas;'))

