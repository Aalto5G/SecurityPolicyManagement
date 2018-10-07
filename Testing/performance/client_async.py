#!/usr/bin/python3.5

import asyncio
import aiohttp
import json
import logging
import time
import sys
import random
import traceback
import ssl
import copy

"""
import cetpManager
import C2CTransaction
import H2HTransaction
import CETPH2H
import CETPC2C
"""

LOGLEVEL_RESTPolicyClient = logging.INFO


# Aiohttp-based PolicyAgent in CES to retrieve CETP policies from Policy Management System
# Leveraging https://stackoverflow.com/questions/37465816/async-with-in-python-3-4


class RESTPolicyClient(object):
    def __init__(self, loop, tcp_conn_limit, verify_ssl=False, name="RESTPolicyClient"):
        self._loop = loop
        self.tcp_conn_limit = tcp_conn_limit
        self.verify_ssl = verify_ssl
        self.policy_cache = {}
        self._logger = logging.getLogger(name)
        self._logger.setLevel(LOGLEVEL_RESTPolicyClient)
        self._logger.info("Initiating RESTPolicyClient towards Policy Management System ")
        self._connect()

    def _connect(self):
        try:
            tcp_conn = aiohttp.TCPConnector(limit=self.tcp_conn_limit, loop=self._loop, verify_ssl=self.verify_ssl)
            self.client_session = aiohttp.ClientSession(connector=tcp_conn)
        except Exception as ex:
            self._logger.error("Failure initiating the rest policy client")
            self._logger.error(ex)

    def close(self):
        self.client_session.close()

    @asyncio.coroutine
    def get(self, url, params=None, timeout=None):
        with aiohttp.Timeout(timeout):
            resp = None  # To handles issues related to connectivity with url
            try:
                #"""
                resp = yield from self.client_session.get(url, params=params)
                policy_response = yield from resp.text()
                #print(policy_response)
                #"""
                #yield from asyncio.sleep(1)


            except Exception as ex:
                # .close() on exception.
                if resp != None:
                    resp.close()
                self._logger.error(ex)
            finally:
                if resp != None:
                    yield from resp.release()  # .release() - returns connection into free connection pool.


def main(policy_client):
    for i in range(0, 2):
        asyncio.ensure_future(policy_client.get('http://127.0.0.1/API/host_policy_user/FQDN/nest0.gwa.demo.'))
        #asyncio.ensure_future(policy_client.get('http://www.google.com'))
        # asyncio.ensure_future(policy_client.get('http://www.thomas-bayer.com/sqlrest/'))
        # yield from asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tcp_conn_limit = 1
    policy_client = RESTPolicyClient(loop, tcp_conn_limit)

    try:
        main(policy_client)
        loop.run_forever()
    except KeyboardInterrupt:
        print('Keyboard Interrupt\n')
    finally:
        # Aiohttp resource cleanup
        loop.stop()
        policy_client.close()
        loop.close()