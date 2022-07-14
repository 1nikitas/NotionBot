import sqlite3

class Database_Notion:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    
    def add_user(self, tg_id, email):
        with self.connection:
            return self.cursor.execute("INSERT INTO Notion(tg_id, email, sub) VALUES (?, ?, ?)", (tg_id, email, 1,))


    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM Notion WHERE tg_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def tg_uesrs(self):
        with self.connection:
            return self.cursor.execute("SELECT tg_id FROM tg")

    def set_unsub(self, tg_id):
        with self.connection:
            return self.cursor.execute("UPDATE Notion  SET sub = ? WHERE tg_id=?", (0, tg_id, ))

    def add_user_tg(self, tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO tg(tg_id, sub) VALUES (?, ?)",
                                       (tg_id, 1,))
    def zero_users(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM tg;")

    def user_exists_tg(self, tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM tg WHERE tg_id = ?", (tg_id,)).fetchall()
            return bool(len(result))

    def trans_users(self, sub ):
        with self.connection:
            result = self.cursor.execute("select * from Notion inner join tg on Notion.tg_id=tg.tg_id where Notion.sub=?; VALUES(?)", (sub,)).fetchall()
            return result


    def id_selector(self):
        with self.connection:
            result = self.cursor.execute(
                "SELECT email from Notion where sub=0;").fetchall()
            return result

    def tg_in_notion(self):
        with self.connection:
            return self.cursor.execute(
                "UPDATE Notion SET sub=1 WHERE Notion.tg_id in (select tg_id from tg)")

    def email_zero(self):
        with self.connection:
           self.cursor.execute(
                "UPDATE Notion SET sub=0")


    def delete_from_notion(self, email):
        with self.connection:
           self.cursor.execute(
                "DELETE from Notion where email = ?", (email,))