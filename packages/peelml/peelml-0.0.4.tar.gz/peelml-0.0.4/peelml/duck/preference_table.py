import os
import duckdb

from peelml.duck.answer_table import AnswerTable
from peelml.duck.question_table import QuestionTable


class PreferenceTable:
    TABLE_NAME = "preference_table"

    def __init__(self):
        # create folder if it doesn't exist
        folder_path = f"{os.getenv('DUCKDB_PATH')}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # connect to duckdb or existing duckdb database
        # or create a new one if it doesn't exist
        self._conn = duckdb.connect(f"{folder_path}/duckdb.db")
        # check if table exists
        result = self._conn.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' "
            f"AND name='{PreferenceTable.TABLE_NAME}'"
        ).fetchall()
        # create a duckdb table if it doesn't exist
        if not result:
            print("creating preference table")
            self._conn.execute("CREATE TYPE VOTE_TYPE AS ENUM ('good', 'bad', 'na')")
            self._conn.execute(
                f"CREATE TABLE {PreferenceTable.TABLE_NAME} ("
                f"id INT64 PRIMARY KEY, "
                f"qid INT64, "
                f"aid INT64, "
                f"vote VOTE_TYPE, "
                f")"
            )
        self._question_table = QuestionTable()
        self._answer_table = AnswerTable()

    def insert(self, **kwargs):
        # increment and return id
        result = self._conn.execute(
            f"SELECT * FROM {PreferenceTable.TABLE_NAME} ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if result:
            id = result[0] + 1
        else:
            id = 1
        if kwargs["vote"] not in ["good", "bad", "na"]:
            raise ValueError(
                f"vote must be one of ['good', 'bad', 'na'], not {kwargs['vote']}"
            )
        qid = self._question_table.insert(question=kwargs["question"])
        aid = self._answer_table.insert(answer=kwargs["answer"])
        # insert id, qid, and aid into table
        query = f"INSERT INTO {PreferenceTable.TABLE_NAME} VALUES ('{id}', '{qid}', '{aid}', '{kwargs['vote']}')"
        self._conn.execute(query)
        # show the tables
        self._conn.sql(f"SELECT * FROM {PreferenceTable.TABLE_NAME}").show()
        self._conn.sql(f"SELECT * FROM {QuestionTable.TABLE_NAME}").show()
        self._conn.sql(f"SELECT * FROM {AnswerTable.TABLE_NAME}").show()
        return id

    def get(self):
        result = self._conn.execute(
            f"""
            SELECT preference.id, question.question, answer.answer, preference.vote
            FROM {PreferenceTable.TABLE_NAME} AS preference
            JOIN {QuestionTable.TABLE_NAME} AS question ON preference.qid = question.qid
            JOIN {AnswerTable.TABLE_NAME} AS answer ON preference.aid = answer.aid
        """
        ).fetchall()
        response = []
        for row in result:
            response.append(
                {
                    "id": row[0],
                    "question": row[1],
                    "answer": row[2],
                    "vote": row[3],
                }
            )
        return response

    def update(self, **kwargs):
        # Execute the SQL query to update the table column based on the primary key
        id = kwargs["id"]
        vote = kwargs["vote"]
        if vote not in ["good", "bad", "na"]:
            raise ValueError(
                f"vote must be one of ['good', 'bad', 'na'], not {kwargs['vote']}"
            )

        check_query = f"SELECT id FROM {PreferenceTable.TABLE_NAME} WHERE id = {id}"
        check_result = self._conn.execute(check_query)

        if len(check_result.fetchall()) == 0:
            raise ValueError(
                f"Row with id {id} does not exist in {PreferenceTable.TABLE_NAME}. Update aborted."
            )
        else:
            self._conn.execute(
                f"UPDATE {PreferenceTable.TABLE_NAME} SET vote = '{vote}' WHERE id = {id}"
            )
