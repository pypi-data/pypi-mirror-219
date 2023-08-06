import threading

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sqldaogenerator.logger.logger import info

default_name = 'default'
transaction_managers = {}


def register_transaction_manager(name: str, transaction_manager):
    transaction_managers.update({name: transaction_manager})


def transactional(func):
    def wrapper(*args, **kwargs):
        if transaction_managers[default_name].is_exists():
            info('Participating in an existing transaction.')
            result = func(*args, **kwargs)
        else:
            info('Creating a new transaction.')
            with transaction_managers[default_name] as session:
                result = func(*args, **kwargs)
                session.commit()
        return result

    return wrapper


class TransactionManager:
    name: str
    session_maker: sessionmaker
    transaction_thread = threading.local()

    def __new__(cls, name: str, datasource):
        instance = super(TransactionManager, cls).__new__(cls)
        if not hasattr(instance, 'session_maker'):
            instance.name = name
            instance.session_maker = sessionmaker(bind=datasource.engine)
        register_transaction_manager(name, instance)
        return instance

    def __enter__(self):
        session = self.session_maker()
        self.transaction_thread.session = session
        self.transaction_thread.is_exists = True
        return session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transaction_thread.session.close()
        self.transaction_thread.is_exists = False

    def is_exists(self):
        return hasattr(self.transaction_thread, 'is_exists') and self.transaction_thread.is_exists

    def get_transaction(self) -> Session:
        if self.is_exists():
            return self.transaction_thread.session
        else:
            raise LookupError('No existing transaction.')

    def new_transaction(self):
        return self.session_maker()
