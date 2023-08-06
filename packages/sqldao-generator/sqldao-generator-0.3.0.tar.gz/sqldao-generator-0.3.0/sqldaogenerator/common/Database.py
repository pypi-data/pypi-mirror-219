from sqldaogenerator.common.TransactionManager import TransactionManager


class Database:
    name: str
    transactionManager: TransactionManager

    def __init__(self, name='default'):
        self.transactionManager = TransactionManager(name, self)
