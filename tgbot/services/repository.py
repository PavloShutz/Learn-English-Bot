class Repo:
    def __init__(self, conn):
        self.conn = conn

    async def create_user_table(self):
        sql = """CREATE TABLE IF NOT EXISTS "users"(
        id BIGINT NOT NULL PRIMARY KEY,
        full_name character varying NOT NULL,
        )
        """
        await self.conn.execute(sql)
