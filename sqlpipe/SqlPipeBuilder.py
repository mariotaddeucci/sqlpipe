import asyncio
import asyncpg
import aiomysql
from glob import iglob
from os import path
from urllib.parse import urlparse
import re


class SqlPipeBuilder:

    def __init__(self, connection, connections_limit=20):
        self.connection = connection
        self.tasks = {}
        self.__pool = None
        self.connections_limit = connections_limit

    async def _pool(self):
        if self.__pool is None:
            dbc = urlparse(self.connection)

            if dbc.scheme.lower() in ['postgres', 'redshift', 'postgresql']:
                self.__pool = await asyncpg.create_pool(
                    user=dbc.username,
                    password=dbc.password,
                    database=dbc.path.lstrip('/'),
                    host=dbc.hostname,
                    port=dbc.port,
                    dsn=self.connection,
                    min_size=1,
                    max_size=self.connections_limit
                )
            elif dbc.scheme.lower() in ['mysql']:
                self.__pool = await aiomysql.create_pool(
                    host=dbc.hostname,
                    port=dbc.port,
                    user=dbc.username,
                    password=dbc.password,
                    db=dbc.path.lstrip('/'),
                    minsize=1,
                    maxsize=self.connections_limit
                )

        return self.__pool

    async def execute_sql(self, sql):
        pool = await self._pool()
        async with pool.acquire() as con:
            await con.execute(sql)

    async def __execute_task(self, task_id):
        task = self.tasks.get(task_id, None)
        if task is None:
            return

        sql_script = task.get('script')
        if task.get('file', False):
            sql_script = open(sql_script, 'r').read()

        await self.execute_sql(sql_script)
        await self.__call_children(task_id)

    async def __call_children(self, parent_id):
        stack = (
            self.__execute_task(task_id)
            for task_id, task in self.tasks.items()
            if task.get('parent_id', None) == parent_id
        )
        await asyncio.gather(*stack)

    async def async_execute(self, task_id=None):
        if task_id:
            await self.__execute_task(task_id)
        else:
            await self.__call_children(None)

    def add_task(self, id, script, parent_id=None, file=False):
        self.tasks.update({
            id: {'script': script, 'parent_id': parent_id, 'file': file}
        })

    def clear_tasks(self):
        self.tasks = {}

    def map_directory(self, directory):
        search = path.join(directory, '**', '*.sql')
        for filename in iglob(search, recursive=True):
            with open(filename) as file:
                dep = re.findall(r".*@parent=(.*).*", file.read())

            parent_id = dep[0] if dep else None
            task_id = filename.replace(directory, '')
            task_id = task_id.replace(path.sep, '.')[:-4]

            self.add_task(
                id=task_id,
                script=filename,
                parent_id=parent_id,
                file=True
            )

    def execute(self, task_id=None):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_execute(task_id))
