import sys
import asyncpg


class Repo:
    def __init__(self, conn):
        self.conn = conn

    async def create_user_table(self):
        sql = """CREATE TABLE IF NOT EXISTS "users"(
        id BIGINT NOT NULL PRIMARY KEY,
        full_name character varying NOT NULL
        )
        """
        await self.conn.execute(sql)

    async def create_dictionary_table(self):
        create_query = """CREATE TABLE IF NOT EXISTS "dictionary"(
        id SERIAL,
        word character varying not null,
        definition character varying not null
        )
        """
        await self.conn.execute(create_query)

    async def create_questions_table(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS "questions"(
        id SERIAL,
        title character varying not null
        )
        """
        await self.conn.execute(create_query)

    async def create_answers_table(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS "answers"(
        id SERIAL,
        title character varying not null,
        question integer not null,
        is_correct boolean not null
        )
        """
        await self.conn.execute(create_query)

    @staticmethod
    def _make_user_insertion_script(**kwargs) -> str:
        insert_query = f"""
            INSERT INTO "users"({', '.join(key for key, _ in kwargs.items())})
            VALUES({', '.join(f"'{value}'" 
        if isinstance(value, str) else str(value) if isinstance(value, int | float) else 'NULL'
        for value in kwargs.values())})
                """
        return insert_query

    async def add_user(self, id: int, name: str) -> None:
        sql_query = self._make_user_insertion_script(id=id, full_name=name)
        try:
            await self.conn.execute(sql_query)
        except (RuntimeError, asyncpg.exceptions.UniqueViolationError):
            pass

    async def add_word_to_dictionary(self, word: str, definition: str) -> None:
        sql = f"""
        INSERT INTO "dictionary"(word, definition) VALUES ('{word}', '{definition}')
        """
        await self.conn.execute(sql)

    async def add_question(self, title: str) -> None:
        sql = f"""
        INSERT INTO "questions"(title) VALUES ('{title}')
        """
        await self.conn.execute(sql)

    async def add_answer(self, title: str, question: int, is_correct: bool) -> None:
        sql = f"""
        INSERT INTO "answers"(title, question, is_correct) VALUES ('{title}', {question}, {is_correct})
        """
        await self.conn.execute(sql)

    async def select_question_id(self, title: str):
        sql = f"""
            SELECT questions."id" from questions WHERE questions.title = '{title}'
        """
        data = await self.conn.fetchrow(sql)
        return data['id']

    async def user_in_table(self, id: int) -> bool:
        sql = f"""
            SELECT users."id" FROM users WHERE users."id" = {id}
        """
        data = await self.conn.fetch(sql)
        return len(data) == 1

    async def get_poll_data(self, id: int):
        sql = f"""SELECT questions.title, answers.title as "text", answers.is_correct FROM questions
            JOIN answers ON answers.question = questions.id
            WHERE questions.id = {id}
        """
        data = await self.conn.fetch(sql)
        question = [q['title'] for q in data][0]
        answers = [{a['text']: a['is_correct']} for a in data]
        return question, answers

    async def get_amount_of_questions(self):
        sql = """SELECT COUNT(id) FROM questions"""
        data = await self.conn.fetchrow(sql)
        return data['count']
