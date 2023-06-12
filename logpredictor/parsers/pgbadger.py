from shutil import which


class PGBadger:
    def __init__(self):
        self.instance = which('pgbadger')
        if not self.instance:
            raise Exception('pgbadger not found')

    def __call__(self):
        return self.instance

# pdbadger = PGBadger()
