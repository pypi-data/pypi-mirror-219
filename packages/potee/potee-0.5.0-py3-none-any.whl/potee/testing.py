import random
from string import ascii_letters
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('checker')

def generate_flag(n=24):
    return "".join(random.choices(ascii_letters, k=n))


class FlagStorage:
    storage: dict() = {}

    def add(self, name, flag, _id):
        self.storage[name] = {"flag": flag, "id": _id}

    def get(self, name):
        return self.storage[name].get("id")

    def validate(self, name, flag, _id):
        return tuple(self.storage[name].values()) == (flag, _id)


class ServiceTesting:
    iterations: int = 3
    actions: list = ["ping", "put", "get", "exploit"]
    host: str = "localhost"
    storage: FlagStorage = FlagStorage()

    def run(self, functions):
        for i in range(1, self.iterations):
            logger.info(f"iteration:{i}")
            for action in self.actions:
                action_functions = functions[action]
                for name, f in action_functions.items():
                    self.__getattribute__(action)(f, name)

    def ping(self, f, name):
        answer = f(self.host)
        if answer == "pong":
            logger.info("ping => pong")
        else:
            logger.error(f"ping => {answer}")

    def put(self, f, name):
        flag = generate_flag()
        _id = f(self.host, flag)
        self.storage.add(name, flag, _id)

        logger.info(f"put:{name}({flag}) => {_id}")

    def get(self, f, name):
        _id = self.storage.get(name)
        flag = f(self.host, _id)
        if self.storage.validate(name, flag, _id):
            logger.info(f"get:{name}({_id}) => {flag}")
        else:
            logger.error(f"get:{name}({_id}) => {flag}")

    def exploit(self, f, name):
        result = f(self.host)
        if result == 1:
           logger.info(f"exploit:{name} => exploitable") 
        elif result == 0:
            logger.info(f"exploit:{name} => not exploitable") 
        else:
            logger.error(f"exploit:{name} => {result}") 
