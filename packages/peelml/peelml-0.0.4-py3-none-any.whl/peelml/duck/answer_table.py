import os
import duckdb


class AnswerTable:
    TABLE_NAME = "answer_table"
    def __init__(self):
        # create folder if it doesn't exist
        folder_path = f"{os.getenv('DUCKDB_PATH')}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # connect to duckdb or existing duckdb database
        # or create a new one if it doesn't exist
        self._conn = duckdb.connect(
            f"{folder_path}/duckdb.db")
        # check if table exists
        result = self._conn.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' "
            f"AND name='{AnswerTable.TABLE_NAME}'").fetchall()
        # create a duckdb table if it doesn't exist
        if not result:
            print("creating answer table")
            self._conn.execute(
                f"CREATE TABLE {AnswerTable.TABLE_NAME} ("
                f"aid INT64 PRIMARY KEY, "
                f"answer STRING, "
                f")")

    def insert(self, **kwargs):
        # increment and return qid
        result = self._conn.execute(f"SELECT * FROM {AnswerTable.TABLE_NAME} ORDER BY aid DESC LIMIT 1").fetchone()
        if result:
            aid = result[0] + 1
        else:
            aid = 1
        # insert aid and answer into table
        query = f"INSERT INTO {AnswerTable.TABLE_NAME} VALUES ('{aid}', '{kwargs['answer']}')"
        self._conn.execute(query)
        return aid
