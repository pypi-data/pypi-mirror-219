import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class Storage:
    """Database handler for internal program data"""

    def __init__(self, base_dir: str):
        self.connection = sqlite3.connect(f'{base_dir}/data.db')
        self.connection.row_factory = dict_factory
        self.initialize()

    def initialize(self):
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session (
                description TEXT,
                cookie_id TEXT,
                is_default INTEGER,
                first_used TEXT
            )
        ''')

        self.connection.commit()

    def get_one_by_id(self, rowid: int) -> dict | None:
        cursor = self.connection.cursor()

        cursor.execute('''
            SELECT rowid, * FROM session
            WHERE rowid = :rowid
        ''', {
            'rowid': rowid
        })

        session = cursor.fetchone()

        if not session:
            return None

        return session

    def get_all(self) -> list:
        cursor = self.connection.cursor()

        cursor.execute('''
            SELECT rowid, * FROM session
        ''')

        return cursor.fetchall()

    def update(self, session: dict):
        cursor = self.connection.cursor()

        cursor.execute('''
            UPDATE session SET
                description = :description,
                cookie_id = :cookie_id,
                is_default = :is_default
            WHERE rowid = :rowid
        ''', {
            'rowid': session['rowid'],
            'description': session['description'],
            'cookie_id': session['cookie_id'],
            'is_default': session['is_default']
        })

        self.connection.commit()

    def insert(self, session: dict) -> int:
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO session (
                description,
                cookie_id,
                is_default,
                first_used
            ) VALUES (
                :description,
                :cookie_id,
                :is_default,
                datetime()
            )
        ''', {
            'description': session['description'],
            'cookie_id': session['cookie_id'],
            'is_default': session['is_default']
        })

        self.connection.commit()

        return cursor.lastrowid

    def reset_default(self):
        cursor = self.connection.cursor()

        cursor.execute('''
            UPDATE session SET
                is_default = 0
        ''')

        self.connection.commit()

    def delete(self, session: dict):
        cursor = self.connection.cursor()

        cursor.execute('''
            DELETE FROM session
            WHERE rowid = :rowid
        ''', {
            'rowid': session['rowid']
        })

        self.connection.commit()
