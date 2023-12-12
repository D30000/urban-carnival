import pypyodbc

class Singleton(type):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ZooObserver:
    def update(self, message):
        print(f"Change in ZooFacade: {message}")

class ZooFacade(metaclass=Singleton):
    def __init__(self, database_path):
        self.database_path = database_path
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def get_table_data(self, table_name):
        conn = pypyodbc.connect(f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.database_path}")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name};")
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()

        conn.close()
        self.notify_observers(f"Table data retrieved for {table_name}")
        return columns, data

    def get_personal_data_by_id(self, personal_id):
        conn = pypyodbc.connect(f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.database_path}")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM ПЕРСОНАЛ WHERE ПЕРСОНАЛ.ID = ?;", (personal_id,))
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()

        conn.close()
        self.notify_observers(f"Personal data retrieved for ID {personal_id}")
        return columns, data
