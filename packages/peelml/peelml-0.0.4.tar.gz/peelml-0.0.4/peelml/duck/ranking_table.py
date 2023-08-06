import os
import duckdb

from peelml.duck.answer_table import AnswerTable
from peelml.duck.question_table import QuestionTable


class RankingTable:
    TABLE_NAME = "ranking_table"
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
            f"AND name='{RankingTable.TABLE_NAME}'").fetchall()
        # create a duckdb table if it doesn't exist
        if not result:
            print("creating ranking table")
            self._conn.execute(
                f"CREATE TABLE {RankingTable.TABLE_NAME} ("
                f"id INT64 PRIMARY KEY, "
                f"qid INT64, "
                f"aid1 INT64, "
                f"aid2 INT64, "
                f")")
        self._question_table = QuestionTable()
        self._answer_table = AnswerTable()

    def insert(self, **kwargs):
        # increment and return id
        result = self._conn.execute(f"SELECT * FROM {RankingTable.TABLE_NAME} ORDER BY id DESC LIMIT 1").fetchone()
        if result:
            id = result[0] + 1
        else:
            id = 1
        qid = self._question_table.insert(question=kwargs['question'])
        aid1 = self._answer_table.insert(answer=kwargs['answer1'])
        aid2 = self._answer_table.insert(answer=kwargs['answer2'])
        # insert id, qid, and aid into table
        query = f"INSERT INTO {RankingTable.TABLE_NAME} VALUES ('{id}', '{qid}', '{aid1}', '{aid2}')"
        self._conn.execute(query)
        return id
