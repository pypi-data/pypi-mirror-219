import os
import duckdb


class QuestionTable:
    TABLE_NAME = "question_table"
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
            f"AND name='{QuestionTable.TABLE_NAME}'").fetchall()
        # create a duckdb table if it doesn't exist
        if not result:
            print("creating question table")
            self._conn.execute(
                f"CREATE TABLE {QuestionTable.TABLE_NAME} ("
                f"qid INT64 PRIMARY KEY, "
                f"question STRING, "
                f")")
    
    def insert(self, **kwargs):
        # increment and return qid
        result = self._conn.execute(f"SELECT * FROM {QuestionTable.TABLE_NAME} ORDER BY qid DESC LIMIT 1").fetchone()
        if result:
            qid = result[0] + 1
        else:
            qid = 1
        # insert qid and question into table
        query = f"INSERT INTO {QuestionTable.TABLE_NAME} VALUES ('{qid}', '{kwargs['question']}')"
        self._conn.execute(query)
        return qid
