from pymongo import MongoClient
import certifi
from config.config import Config

class Connection:
    _client = None
    _db = None
    _key_col = None
    _logs_col=None

    @classmethod
    def get_client(cls):
        """Create a MongoDB client connection."""
        if cls._client is None:
            try:
                print("Attempting to connect to MongoDB...")
                ca = certifi.where()
                # cls._client = MongoClient(Config.mongoUri)
                cls._client=MongoClient(Config.db_Host,int(Config.db_port))
                cls._client.admin.command('ping') 
                print("Successfully connected to MongoDB!")
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                cls._client = None
        return cls._client

    @classmethod
    def get_db(cls):
        """Get the MongoDB database."""
        if cls._db is None:
            client = cls.get_client()
            if client:
                cls._db = client['tradeView'] 
                print("Connected to database 'tradeView'.")
            else:
                print("MongoDB client is not connected.")
        return cls._db

    @classmethod
    def get_key_col(cls):
        """Get the keyCollection collection."""
        
        if cls._key_col is None:
            db = cls.get_db()
            if db is not None:
                cls._key_col = db['keyCollection'] 
                print("Accessed collection 'keyCollection'.")
            else:
                print("Database 'tradeView' is not accessible.")
        return cls._key_col
    @classmethod
    def get_logs_col(cls):
        """Get the logs collection."""
        
        if cls._logs_col is None:
            db = cls.get_db()
            if db is not None:
                cls._logs_col = db['logs'] 
                print("Accessed collection 'Logs'.")
            else:
                print("Database 'tradeView' is not accessible.")
        return cls._logs_col

