import datetime
from peewee import SQL, DateTimeField, Model
from playhouse.sqliteq import SqliteQueueDatabase

db = SqliteQueueDatabase('database/phyrexia.db', autostart=True, timeout=10, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64
})



class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(constraints=[SQL("DEFAULT (datetime('now'))")], default=datetime.datetime.now())
    
    class Meta:
        database = db

def initialize_db(to_create: list):
    try:
        db.connect()
        db.create_tables(to_create, safe=True)
    except Exception as exc:
        print(exc)