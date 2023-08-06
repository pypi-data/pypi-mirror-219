from autonomous.db.autodb import Database
from autonomous.model.orm import ORM
import os
import sys


class DnDORM(ORM):
    def __init__(self, table):
        self.db = Database(path=f"/{os.path.dirname(sys.modules[__name__].__file__)}/")
        self._table = self.db.get_table(table=table)
