import mysql.connector
import pytest

from app import cur, con


def test_database_connection():
    assert isinstance(con, mysql.connector.MySQLConnection)


def test_create_user_table():
    cur.execute("SELECT * FROM User")
    result = cur.fetchall()
    assert len(result) == 0


def test_create_upload_table():
    cur.execute("SELECT * FROM upload")
    result = cur.fetchall()
    assert len(result) == 0
