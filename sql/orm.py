"""Custom mini-ORM: maps Python classes <-> SQLite rows, CRUD <-> DML.
OOP: Encapsulation (Database hides sqlite3), Inheritance (Model base),
     Abstraction (CRUD interface), Polymorphism (per-model table/fields).
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("school.db")


class Database:
    """Encapsulates connection handling (abstraction over sqlite3)."""

    def __init__(self, path=DB_PATH):
        self.path = str(path)

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def execute(self, sql, params=()):
        with self._connect() as conn:
            cur = conn.execute(sql, params)
            return cur.lastrowid

    def fetch_all(self, sql, params=()):
        with self._connect() as conn:
            return [dict(r) for r in conn.execute(sql, params).fetchall()]

    def fetch_one(self, sql, params=()):
        with self._connect() as conn:
            row = conn.execute(sql, params).fetchone()
            return dict(row) if row else None


db = Database()


class Model:
    """Abstract base: subclass sets __table__ and __fields__ (excluding id)."""
    __table__ = ""
    __fields__ = ()

    def __init__(self, id=None, **kwargs):
        self.id = id
        for f in self.__fields__:
            setattr(self, f, kwargs.get(f))

    @classmethod
    def _db(cls):
        return db

    @classmethod
    def create(cls, **kwargs):
        """INSERT INTO {table} (...) VALUES (...)  -- C in CRUD."""
        obj = cls(**kwargs)
        obj.save()
        return obj

    def save(self):
        cols = ", ".join(self.__fields__)
        placeholders = ", ".join("?" for _ in self.__fields__)
        values = [getattr(self, f) for f in self.__fields__]
        self.id = self._db().execute(
            f"INSERT INTO {self.__table__} ({cols}) VALUES ({placeholders})", values
        )
        return self

    @classmethod
    def get(cls, id):
        """SELECT * FROM {table} WHERE id=?  -- R in CRUD."""
        row = cls._db().fetch_one(f"SELECT * FROM {cls.__table__} WHERE id=?", (id,))
        return cls(**row) if row else None

    @classmethod
    def all(cls):
        rows = cls._db().fetch_all(f"SELECT * FROM {cls.__table__} ORDER BY id")
        return [cls(**r) for r in rows]

    @classmethod
    def filter(cls, where, params=()):
        rows = cls._db().fetch_all(f"SELECT * FROM {cls.__table__} WHERE {where}", params)
        return [cls(**r) for r in rows]

    def update(self, **kwargs):
        """UPDATE {table} SET ... WHERE id=?  -- U in CRUD."""
        for k, v in kwargs.items():
            if k in self.__fields__:
                setattr(self, k, v)
        sets = ", ".join(f"{f}=?" for f in self.__fields__)
        values = [getattr(self, f) for f in self.__fields__] + [self.id]
        self._db().execute(f"UPDATE {self.__table__} SET {sets} WHERE id=?", values)
        return self

    def delete(self):
        """DELETE FROM {table} WHERE id=?  -- D in CRUD."""
        self._db().execute(f"DELETE FROM {self.__table__} WHERE id=?", (self.id,))

    def to_dict(self):
        return {"id": self.id, **{f: getattr(self, f) for f in self.__fields__}}

    def __repr__(self):
        fields = ", ".join(f"{f}={getattr(self, f)!r}" for f in self.__fields__)
        return f"{type(self).__name__}(id={self.id!r}, {fields})"
