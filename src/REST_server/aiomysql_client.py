"""
BSD 3-Clause License
Copyright (c) 2018, Muhammad Hassaan Bin Mohsin, Aalto University, Finland
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import aiomysql

from errorsfile import ForbiddenSQLQuery


MYSQL_PORT = 3306



class MySQLClient(object):
    def __init__(self, host, port, user, password, database):
        '''
        Initialize database connection parameters
        :param host: IP of MySQL DB (in my case 127.0.0.1)
        :param port: TCP port of MySQL DB
        :param user: User that will connect to database
        :param password: Password to connect to database
        :param database: Name of database to connect
        '''
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    async def connect(self):
        '''
        Create Pool of connections to database
        '''
        self.pool = await aiomysql.create_pool(host=self.host, port=self.port,
                                               user=self.user, password=self.password,
                                               db=self.database,
                                               minsize=1, maxsize=20)

    async def close(self):
        '''
        Closing all connections
        '''
        self.pool.close()
        await self.pool.wait_closed()

    async def execute(self, query, check=True):
        '''
        Only executes the SQL query.
        It may throw exceptions, e.g. pymysql.err.ProgrammingError
        Returns None.
        :param query: SQL statement
        :param check: True if need to check for special characters in SQL query
        :return: Nothing or raise error
        '''
        if check:
            self._check_sql_query(query)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                return await conn.commit()

    async def fetchall(self, query, check=True):
        '''
        Executes the SQL query and fetchall(). Returns the following:
           On success: returns an iterable of results i.e. (('723162224029077991',),)
           On failure: returns an empty iterable i.e. ()
        :param query: SQL statement
        :param check: True if need to check for special characters in SQL query
        :return: None or All data retrieved for query or raise error
        '''
        if check:
            self._check_sql_query(query)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
                await cur.execute(query)
                # Return iterable result, might be empty
                return await cur.fetchall()

    async def fetchone(self, query, check=True):
        '''
        Executes the SQL query and fetchone(). Returns the following:
            On success: returns an tuple of the result i.e. (9, '723162224029077991', 'Prepaid')
            On failure: returns None
        :param query: SQL statement
        :param check: True if need to check for special characters in SQL query
        :return: None or Single row retrieved for query or raise error
        '''
        if check:
            self._check_sql_query(query)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
                await cur.execute(query)
                # Return the result, might be None
                return await cur.fetchone()

    def _check_sql_query(self, query):
        '''
        Function to check if special or forbidden characters are present in query
        :param query: Sql statement
        : raise error or return nothing in case of no forbidden character found
        '''
        sqlInjectionChar = [';', '%', '&', '^']
        for c in sqlInjectionChar:
            if c in query:
                raise ForbiddenSQLQuery(1007, 'Forbidden character in SQL query "{}"'.format(c))

