import sqlite3

class Database:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.c = self.conn.cursor()
    #---------------------------Table_Commands------------------------------------
    def create_table(self, columns):
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS "BaseData" ({columns})""")
        self.conn.commit()

    def insert_in_table(self, values):
        self.c.execute(f"""INSERT INTO "BaseData" VALUES ({','.join('?' for _ in values)})""", values)
        self.conn.commit()

    def update_table(self, column, value, condition):
        self.c.execute(f"""UPDATE "BaseData" SET {column} = {column} + ? WHERE {condition}""", (value,))
        self.conn.commit()
        
    #---------------------------Non_commit_commands------------------------------------
    def find_user(self, userid):
        return self.fetch_one(f"BaseData, userid = {userid}")

    #---------------------------Fetch_Commands------------------------------------
    def fetch_one(self,condition):
        self.c.execute(f"""SELECT * FROM "BaseData" WHERE {condition}""")
        return self.c.fetchone()
 
    def fetch_many(self,condition):
        self.c.execute(f"""SELECT * FROM "BaseData" WHERE {condition}""")
        return self.c.fetchmany()
    
    def fetch_all(self, condition):
        self.c.execute(f"""SELECT * FROM "BaseData" WHERE {condition}""")
        return self.c.fetchall()
    
    #--------------------------------ARCHIVE---------------------------------------
    #def create_newbasetable(self,  , column, value, condition):
    #    self.c.execute(f""BaseData",userid int, wallet int, bank int")
    
    

    #-------CLOSE--------
    def close(self):
        self.conn.close()











