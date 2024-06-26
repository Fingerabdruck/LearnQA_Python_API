import os

class Environment:
    DEV = 'dev',
    PROD = 'prod'

    URL = {
        DEV: '',
        PROD: ''
    }

    def __init__(self):
        try:
            self.env = os.environ['ENV']
        except KeyError:
            self.env = self.DEV

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Uknown value of ENV variable {self.env}")

ENV_OBJECT = Environment()