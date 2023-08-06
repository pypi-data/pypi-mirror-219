from collections import defaultdict
from typing import Any
from .testing import ServiceTesting
import sys
from aiohttp import ClientSession
import asyncio
import json


class Checker:
    def __init__(self) -> None:
        self.checkers = defaultdict(dict)
        self.filename = ""

    def ping(self, method):
        def inner(f):
            self.register(f, "ping", method, "default")

        return inner

    def get(self, name, method):
        def inner(f):
            self.register(f, "get", method, name)

        return inner

    def put(self, name, method):
        def inner(f):
            self.register(f, "put", method, name)

        return inner

    def exploit(self, name, method):
        def inner(f):
            self.register(f, "exploit", method, name)

        return inner

    def register(self, f, action, method, name):
        self.checkers[action][name] = (getattr(self, method), (f, action))

    def load_data(self):
        with open(self.filename) as f:
            return json.loads(f.read())

    @staticmethod
    async def add_id(f, i, *args):
        try:
            result = await f(*args)
        except Exception as e:
            return {"status": 1, "id": i, "answer": f"error: {type(e)}{e}"}
        return {"status": 0, "id": i, "answer": result}

    def http(self, f, action):
        data = self.load_data()
        tasks = []

        async def decorator():
            async with ClientSession() as session:
                for host in data:
                    if action == "ping" or action == "exploit":
                        func = self.add_id(f, host.get("id"), session, host.get("host"))
                    elif action == "put":
                        func = self.add_id(
                            f,
                            host.get("id"),
                            session,
                            host.get("host"),
                            host.get("flag"),
                        )
                    elif action == "get":
                        func = self.add_id(
                            f,
                            host.get("id"),
                            session,
                            host.get("host"),
                            host.get("value"),
                        )

                    task = asyncio.ensure_future(func)
                    tasks.append(task)

                responses = await asyncio.gather(*tasks, return_exceptions=False)
                return responses

        return decorator

    def run(self):
        action = sys.argv[1]
        self.filename = sys.argv[len(sys.argv) - 1]
        name = "default"
        if len(sys.argv) > 3:
            name = sys.argv[2]
        wrap, data = self.checkers[action][name]
        results = asyncio.run(wrap(*data)())
        print(json.dumps(results))
        # print(self.checkers)
        # print(asyncio.run(self.checkers[0]()))
